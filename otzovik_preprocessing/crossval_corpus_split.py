import codecs
import json
import os
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split

EFFICIENCY_LABEL_TO_ID = {
    "NEUTRAL": 0,
    "EF": 1,
    "INF": 2
}


def write_samples_to_file(output_file, header=False, **kwargs):
    data_df = pd.DataFrame.from_dict(kwargs, )
    data_df.reset_index()
    data_df.to_csv(output_file, sep='\t', quoting=3, index=False, header=header)


def load_sentences_labels(json_fname):
    with codecs.open(json_fname, "r", encoding="utf-8") as json_file:
        sentences = []
        label_ids = []
        doc_ids = []
        sent_ids = []
        data = json.load(json_file)
        for sentence in data:
            doc_id = int(sentence['id'])
            sent_id = int(sentence['sent_id'])
            efficiency_label = sentence['type']
            efficiency_label_id = EFFICIENCY_LABEL_TO_ID[efficiency_label]
            sentence_text = sentence['text']

            doc_ids.append(doc_id)
            sent_ids.append(sent_id)
            sentences.append(sentence_text)
            label_ids.append(efficiency_label_id)

        doc_ids = np.array(doc_ids)
        sent_ids = np.array(sent_ids)
        sentences = np.array(sentences)
        label_ids = np.array(label_ids)
    return sentences, label_ids, doc_ids, sent_ids


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_json', required=True)
    parser.add_argument('--n_splits', type=int, default=5)
    parser.add_argument('--output_directory', required=True)
    args = parser.parse_args()

    crossval_corpus_directory = args.output_directory
    if not os.path.exists(crossval_corpus_directory):
        os.makedirs(crossval_corpus_directory)

    sentences, label_ids, doc_ids, sent_ids = load_sentences_labels(args.input_json)

    kf = KFold(n_splits=args.n_splits)
    for ind, (train_index, test_index) in enumerate(kf.split(sentences)):
        print(f"Creating split {ind}")
        test_doc_ids, test_sent_ids = doc_ids[test_index], sent_ids[test_index]
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
            write_samples_to_file(output_file=train_file, label_id=train_label_ids, text=train_sentences, )
            write_samples_to_file(output_file=dev_file, label_id=dev_label_ids, text=dev_sentences, )
            write_samples_to_file(output_file=test_file, label_id=test_labels_ids, doc_id=test_doc_ids,
                                  sent_id=test_sent_ids, text=test_sentences, header=True)
        print(f"Split {ind} succesfully created")


if __name__ == '__main__':
    main()
