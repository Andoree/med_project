import codecs
import json
import os
from argparse import ArgumentParser

import numpy as np
from sklearn.model_selection import KFold

EFFICIENCY_LABEL_TO_ID = {
    "NEUTRAL" : 0,
    "EF" : 1,
    "INF" : 2
}

def write_samples_to_file(output_file, sentences, labels):
    for ind in range(len(sentences)):
        sentence_text = sentences[ind]
        sentence_label = labels[ind]
        output_file.write(f'{sentence_label}\t{sentence_text}\n')


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_json', required=True)
    parser.add_argument('--n_splits', type=int, default=5)
    parser.add_argument('--output_directory', required=True)
    args = parser.parse_args()

    crossval_corpus_directory = args.output_directory
    if not os.path.exists(crossval_corpus_directory):
        os.makedirs(crossval_corpus_directory)
    with codecs.open(args.input_json, "r", encoding="utf-8") as json_file:
        sentences = []
        label_ids = []
        data = json.load(json_file)
        for sentence in data:
            efficiency_label = sentence['type']
            efficiency_label_id = EFFICIENCY_LABEL_TO_ID[efficiency_label]
            sentence_text = sentence['text']
            sentences.append(sentence_text)
            label_ids.append(efficiency_label_id)

        sentences = np.array(sentences)
        label_ids = np.array(label_ids)
        kf = KFold(n_splits=args.n_splits)
        for ind, (train_index, test_index) in enumerate(kf.split(sentences)):
            print(f"Creating split {ind}")
            train_sentences, train_label_ids = sentences[train_index], label_ids[train_index]
            test_sentences, test_labels_ids = sentences[test_index], label_ids[test_index]
            assert len(train_sentences) == len(train_label_ids)
            assert len(test_sentences) == len(test_labels_ids)
            fold_directory = os.path.join(crossval_corpus_directory, f'fold_{ind}/')
            if not os.path.exists(fold_directory):
                os.makedirs(fold_directory)
            train_path = os.path.join(fold_directory, f'train.tsv')
            test_path = os.path.join(fold_directory, f'test.tsv')
            with codecs.open(train_path, "w+", encoding="utf-8") as train_file, \
                    codecs.open(test_path, "w+", encoding="utf-8") as test_file:
                write_samples_to_file(output_file=train_file, sentences=train_sentences, labels=train_label_ids)
                write_samples_to_file(output_file=test_file, sentences=test_sentences, labels=test_labels_ids)
            print(f"Split {ind} succesfully created")


if __name__ == '__main__':
    main()
