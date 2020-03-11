import codecs
import os
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

from crossval_corpus_split import load_sentences_labels

ID_TO_EFFICIENCY_LABEL = {
    0: "NEUTRAL",
    1: "EF",
    2: "INF"
}


def main():
    parser = ArgumentParser()
    parser.add_argument('--classes_folder', required=True)
    parser.add_argument('--num_folds', type=int, default=5)
    parser.add_argument('--sentences_json', required=True)
    args = parser.parse_args()

    kf = KFold(n_splits=args.num_folds)
    sentence_texts, label_ids = load_sentences_labels(args.sentences_json)
    print(len(sentence_texts))
    assert len(sentence_texts) == len(label_ids)
    human_markup_labels = [ID_TO_EFFICIENCY_LABEL[label_ids[i]] for i in range(len(sentence_texts))]
    # human_markup_labels = {i: ID_TO_EFFICIENCY_LABEL[label_ids[i]] for i in range(len(sentence_texts))}
    predicted_labels = {}
    for ind, (train_index, test_index) in enumerate(kf.split(sentence_texts)):
        print(ind, len(train_index), len(test_index))
        fold_fname = f'fold_{ind}.tsv'
        fold_path = os.path.join(args.classes_folder, fold_fname)
        print(fold_fname)
        with codecs.open(fold_path, "r", encoding="utf-8") as fold_file:
            for sent_number, line in enumerate(fold_file):
                global_sent_id = test_index[sent_number]
                class_probabilities = [float(x) for x in line.split()]
                class_id = np.argmax(class_probabilities)
                predicted_eff_label = ID_TO_EFFICIENCY_LABEL[class_id]
                predicted_labels[global_sent_id] = predicted_eff_label
            #     print(class_id, line)
            # print('--\n' * 4)
    predicted_labels_list = [predicted_labels[sent_id] for sent_id in sorted(predicted_labels.keys())]

    eff_labels_df = pd.DataFrame.from_dict(
        {'text': sentence_texts, 'human_label': human_markup_labels, 'predicted_label': predicted_labels_list})
    mismatched_labels_df = eff_labels_df[eff_labels_df.human_label != eff_labels_df.predicted_label]


    # for sent_id in sorted(predicted_labels.keys(), key=lambda x: -x):
    #     print(sent_id)
    # print(len(predicted_labels.keys()))
    # for k, v in predicted_labels.items():
    #     print(k, v)


if __name__ == '__main__':
    main()
