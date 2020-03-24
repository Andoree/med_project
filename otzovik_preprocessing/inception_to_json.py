import codecs
import json
import os
import random
import re
import shutil
from argparse import ArgumentParser
from sys import stderr

import pandas as pd

EFFICIENCY_LABEL_PATTERN = r'^(?P<status>INF|EF)\[\d+\]$'
MULTICLASS_EFFICIENCY_PATTERN = r'^(EF\[\d+\]\|INF\[\d+\])|(INF\[\d+\]\|EF\[\d+\])$'
DI_ADR_OTHER_PATTERN = r'^(DI|ADR|Other)\[\d+\]$'
ALL_ANNOTATIONS_PATTERN = r'^((DI|ADR|Other|(?P<status>INF|EF))\[\d+\]\|?)+$'


def load_sentence_texts(file_path):
    texts = {}
    with codecs.open(file_path, 'r', encoding='utf-8') as inp:
        sentence_counter = 0
        for line in inp:
            if line.startswith('#Text='):
                sentence_counter += 1
                texts[sentence_counter] = line[6:].strip()
    return texts


def add_sentence_to_datalist(data, sentence_id, sentence_texts, sentences_starts, sentences_ends, efficiency_label,
                             review_id):
    sentence_text = sentence_texts[sentence_id]
    sentence_start = sentences_starts[sentence_id]
    sentence_end = sentences_ends[sentence_id]
    assert len(sentence_text) == sentence_end - sentence_start
    sentence = {
        'text': sentence_text,
        'start': int(sentence_start),
        'end': int(sentence_end),
        'type': efficiency_label,
        'id': int(review_id),
        'sent_id': int(sentence_id)
    }
    data.append(sentence)


def copy_multiclass_file(mulclass_files_folder, review_folder, file_path):
    mulclass_review_folder = os.path.join(mulclass_files_folder, review_folder)
    if not os.path.exists(mulclass_review_folder):
        os.makedirs(mulclass_review_folder)
    mulclass_fname = os.path.join(mulclass_review_folder, 'admin.tsv')
    shutil.copy2(file_path, mulclass_fname)


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_folder', required=True)
    parser.add_argument('--save_to', required=True)
    parser.add_argument('--multiclass_folder', required=True, help='directory for files with multiclass sentences '
                                                                   '(sentences that have both INF and EF annotations)')
    args = parser.parse_args()
    data = []
    multiclass_files_folder = args.multiclass_folder
    for review_folder in os.listdir(args.input_folder):
        review_id = int(review_folder.split('.')[0])
        file_path = os.path.join(args.input_folder, review_folder, 'admin.tsv')
        if not os.path.exists(file_path):
            stderr.write(f"FILE DOES NOT EXIST: {file_path}\n")
            continue
        try:
            sentence_texts = load_sentence_texts(file_path=file_path)
            annotation_data = pd.read_csv(file_path, sep='\t', skip_blank_lines=True, comment='#', encoding='utf-8',
                                          names=['token_id', 'token_span', 'token', 'entity_id', 'entity_type',
                                                 'unknown_1',
                                                 'efficiency'], usecols=range(7), quoting=3)
            annotation_data['sentence_id'] = annotation_data.token_id.apply(lambda tid: int(tid.split('-')[0]))
            annotation_data['start'] = annotation_data.token_span.apply(lambda tid: int(tid.split('-')[0]))
            annotation_data['end'] = annotation_data.token_span.apply(lambda tid: int(tid.split('-')[1]))
            sentences_starts = annotation_data.groupby('sentence_id')['start'].min()
            sentences_ends = annotation_data.groupby('sentence_id')['end'].max()

            annotated_sentences_ids = set()
            effiency_sentence_flag = False
            for row in annotation_data.iterrows():
                row_series = row[1]
                efficiency_annotation = row_series['efficiency']
                sentence_id = row_series['sentence_id']

                if sentence_id in annotated_sentences_ids:
                    continue

                m = re.fullmatch(EFFICIENCY_LABEL_PATTERN, efficiency_annotation)
                if m is not None:
                    efficiency_label = m.group('status')
                    effiency_sentence_flag = True
                    annotated_sentences_ids.add(sentence_id)
                    add_sentence_to_datalist(data=data, sentence_id=sentence_id, sentence_texts=sentence_texts,
                                             sentences_starts=sentences_starts, sentences_ends=sentences_ends,
                                             efficiency_label=efficiency_label, review_id=review_id)
                    annotated_sentences_ids.add(sentence_id)
                elif re.fullmatch(MULTICLASS_EFFICIENCY_PATTERN, efficiency_annotation):
                    annotated_sentences_ids.add(sentence_id)
                    copy_multiclass_file(mulclass_files_folder=multiclass_files_folder, review_folder=review_folder,
                                         file_path=file_path)
                elif re.fullmatch(DI_ADR_OTHER_PATTERN, efficiency_annotation) or len(
                        efficiency_annotation.split('|')) == 3:
                    annotated_sentences_ids.add(sentence_id)
                elif re.fullmatch(ALL_ANNOTATIONS_PATTERN, efficiency_annotation):
                    m = re.fullmatch(ALL_ANNOTATIONS_PATTERN, efficiency_annotation)
                    print(review_folder, efficiency_annotation)
                    efficiency_label = m.group('status')
                    effiency_sentence_flag = True
                    annotated_sentences_ids.add(sentence_id)
                    add_sentence_to_datalist(data=data, sentence_id=sentence_id, sentence_texts=sentence_texts,
                                             sentences_starts=sentences_starts, sentences_ends=sentences_ends,
                                             efficiency_label=efficiency_label, review_id=review_id)
                    annotated_sentences_ids.add(sentence_id)
                else:
                    if not efficiency_annotation == '_':
                        print("Annotation", f"{efficiency_annotation}")
                    assert efficiency_annotation == '_'
            if effiency_sentence_flag:
                sent_ids = set(annotation_data['sentence_id'].unique())
                not_annotated_sent_ids = sent_ids.difference(annotated_sentences_ids)
                not_annot_sent_id = random.choice(tuple(not_annotated_sent_ids))

                add_sentence_to_datalist(data=data, sentence_id=not_annot_sent_id, sentence_texts=sentence_texts,
                                         sentences_starts=sentences_starts, sentences_ends=sentences_ends,
                                         efficiency_label='NEUTRAL', review_id=review_id)
        except pd.errors.ParserError as err:
            err_msg = str(err)
            if err_msg == 'Too many columns specified: expected 7 and found 6':
                stderr.write(f'File is not properly annotated: {file_path}\n')
            else:
                stderr.write(f'{err_msg}\n')

    with open(args.save_to, 'w', encoding='utf-8') as output:
        serialized_data = json.dumps(data, ensure_ascii=False)
        output.write(serialized_data + '\n')


if __name__ == '__main__':
    main()
