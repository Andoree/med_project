import codecs
import os
import random
from argparse import ArgumentParser
from sys import stderr

import pandas as pd
import re
import json

EFFICIENCY_LABEL_PATTERN = r'^(?P<status>INF|EF)\[\d+\]$'
AMBIGOUS_EFFICIENCY_PATTERN = r'^(EF\[\d+\]\|INF\[\d+\])|(INF\[\d+\]\|EF\[\d+\])$'
# TODO:
RE_PATTERN = r'^(DI|ADR|Other)\[\d+\]$'

# todo: Сделать словарём, по ключу получать строку
# todo: Проверить, что индексы здесь и там правильные
# todo: Ввести счётчик строк с началом "#Text=",
# todo: Ключ в словарь подсчитывать исходя из этого индекса
def load_sentence_texts(file_path):
    texts = {}
    with codecs.open(file_path, 'r', encoding='utf-8') as inp:
        sentence_counter = 0
        #line = [line for line in inp]
        for line in inp:
            if line.startswith('#Text='):
                sentence_counter += 1
                texts[sentence_counter] = line[6:].strip()
                # texts.append(line[6:].strip())
                #
                # if line[6:].strip().startswith('2.'):
                #     print(file_path)
                #     print(line)
                #     print('--')
    return texts


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input_folder')
    parser.add_argument('--save_to')
    args = parser.parse_args()
    data = []
    for review_folder in os.listdir(args.input_folder):
        print(review_folder)
        review_id = int(review_folder.split('.')[0])
        file_path = os.path.join(args.input_folder, review_folder, 'admin.tsv')
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

            # added_sentences_ids = set()
            annotated_sentences_ids = set()
            effiency_sentence_flag = False
            sentences_count = annotation_data['sentence_id'].max()
            for row in annotation_data.iterrows():
                row_series = row[1]
                token = row_series['token']
                efficiency_annotation = row_series['efficiency']
                sentence_id = row_series['sentence_id']

                if sentence_id in annotated_sentences_ids:
                    continue

                m = re.fullmatch(EFFICIENCY_LABEL_PATTERN, efficiency_annotation)
                if m is not None:
                    efficiency_label = m.group('status')
                    effiency_sentence_flag = True
                    annotated_sentences_ids.add(sentence_id)
                    sentence_text = sentence_texts[sentence_id]
                    token_start = sentences_starts[sentence_id]
                    token_end = sentences_ends[sentence_id]

                    sentence = {
                        'text': sentence_text,
                        'start': token_start,
                        'end': token_end,
                        'type': efficiency_label,
                        'id': review_id,
                        'sent_id': sentence_id
                    }
                    data.append(sentence)
                    annotated_sentences_ids.add(sentence_id)
                # todo: такие кейсы удалить из рассмотрения, не давать им быть рандомными
                # todo: NEUTRAL
                elif re.fullmatch(AMBIGOUS_EFFICIENCY_PATTERN, efficiency_annotation):
                    print(efficiency_annotation)
                    pass
                elif re.fullmatch(RE_PATTERN, efficiency_annotation):
                    print('Case 3', efficiency_annotation)
                    pass
                elif review_folder == '811884.tsv':
                    print(':(')
                    pass
                else:
                    # print(efficiency_annotation)
                    assert efficiency_annotation == '_'
            if effiency_sentence_flag:
                sent_ids = set([i + 1 for i in range(sentences_count)])
                not_annotated_sent_ids = sent_ids.difference(annotated_sentences_ids)
                not_annot_sent_id = random.choice(tuple(not_annotated_sent_ids))

                sent_text = sentence_texts[not_annot_sent_id]
                token_start = sentences_starts[not_annot_sent_id]
                token_end = sentences_ends[not_annot_sent_id]
                assert len(sent_text) == token_end - token_start

                sentence = {
                    'text': sent_text,
                    'start': token_start,
                    'end': token_end,
                    'type': 'NEUTRAL',
                    'id': review_id,
                    'sent_id': not_annot_sent_id
                }
                data.append(sentence)
            # for d in data:
            #     print(d['text'])
            #     print('\t', d['start'])
            #     print('\t', d['end'])
            #     print('\t', d['type'])
            #     print('\t', d['id'])
            #     print('\t', d['sent_id'])



        except pd.errors.ParserError as err:
            err_msg = str(err)
            if err_msg == 'Too many columns specified: expected 7 and found 6':
                stderr.write(f'File is not properly annotated: {file_path}\n')
            else:
                stderr.write(f'{err_msg}\n')
        except KeyError as err:
            err_msg = str(err)
    # TODO: Fix serialization
    # TODO: Добавить директорию неоднозначных случаев
    with open(args.save_to, 'w', encoding='utf-8') as output:
        serialized_data = json.dumps(data, ensure_ascii=False)
        output.write(serialized_data + '\n')
