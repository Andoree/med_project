import codecs
import json
import os
from argparse import ArgumentParser

import numpy as np
from sklearn.model_selection import KFold, train_test_split

EFFICIENCY_LABEL_TO_ID = {
    "NEUTRAL": 0,
    "EF": 1,
    "INF": 2
}


def write_samples_to_file(output_file, sentences, labels, header=False):
    if header:
        output_file.write(f'label_id\ttext\n')
    for ind in range(len(sentences)):
        sentence_text = sentences[ind]
        sentence_label = labels[ind]
        output_file.write(f'{sentence_label}\t{sentence_text}\n')


def load_sentences_labels(json_fname):
    with codecs.open(json_fname, "r", encoding="utf-8") as json_file:
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
    return sentences, label_ids


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_json', required=True)
    parser.add_argument('--n_splits', type=int, default=5)
    parser.add_argument('--output_directory', required=True)
    args = parser.parse_args()

    crossval_corpus_directory = args.output_directory
    if not os.path.exists(crossval_corpus_directory):
        os.makedirs(crossval_corpus_directory)

    sentences, label_ids = load_sentences_labels(args.input_json)

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
        train_path = os.path.join(fold_directory, 'train.tsv')
        train_sentences, dev_sentences, train_label_ids, dev_label_ids = \
            train_test_split(train_sentences, train_label_ids, test_size=0.1, random_state=42)
        dev_path = os.path.join(fold_directory, 'dev.tsv')
        test_path = os.path.join(fold_directory, 'test.tsv')
        with codecs.open(train_path, "w+", encoding="utf-8") as train_file, \
                codecs.open(test_path, "w+", encoding="utf-8") as test_file, \
                codecs.open(dev_path, "w+", encoding="utf-8") as dev_file:
            write_samples_to_file(output_file=train_file, sentences=train_sentences, labels=train_label_ids)
            write_samples_to_file(output_file=dev_file, sentences=dev_sentences, labels=dev_label_ids)
            write_samples_to_file(output_file=test_file, sentences=test_sentences, labels=test_labels_ids, header=True)
        print(f"Split {ind} succesfully created")


if __name__ == '__main__':
    main()
