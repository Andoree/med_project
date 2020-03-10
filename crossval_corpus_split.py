import codecs
import json
import os
from argparse import ArgumentParser
from sklearn.model_selection import KFold
import numpy as np


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
        labels = []
        data = json.load(json_file)
        for sentence in data:
            efficiency_label = sentence['type']
            sentence_text = sentence['text']
            sentences.append(sentence_text)
            labels.append(efficiency_label)

        sentences = np.array(sentences)
        labels = np.array(labels)
        kf = KFold(n_splits=args.n_splits)
        for ind, (train_index, test_index) in enumerate(kf.split(sentences)):
            print(f"Creating split {ind}")
            train_sentences, train_labels = sentences[train_index], labels[train_index]
            test_sentences, test_labels = sentences[test_index], labels[test_index]
            assert len(train_sentences) == len(train_labels)
            assert len(test_sentences) == len(test_labels)
            train_path = os.path.join(crossval_corpus_directory, f'train_{ind}.tsv')
            test_path = os.path.join(crossval_corpus_directory, f'test_{ind}.tsv')
            with codecs.open(train_path, "w+", encoding="utf-8") as train_file, \
                    codecs.open(test_path, "w+", encoding="utf-8") as test_file:
                write_samples_to_file(output_file=train_file, sentences=train_sentences, labels=train_labels)
                write_samples_to_file(output_file=test_file, sentences=test_sentences, labels=test_labels)
            print(f"Split {ind} succesfully created")

if __name__ == '__main__':
    main()
