import codecs
import os
from argparse import ArgumentParser

import numpy as np
import pandas as pd

ID_TO_EFFICIENCY_LABEL = {
    0: "NEUTRAL",
    1: "EF",
    2: "INF"
}


def main():
    parser = ArgumentParser()
    parser.add_argument('--classes_folder', required=True)
    parser.add_argument('--num_folds', type=int, default=5)
    parser.add_argument('--kfold_dir', required=True)
    parser.add_argument('--save_to', required=True)
    args = parser.parse_args()

    doc_ids = []
    sent_ids = []
    sentence_texts = []
    human_labels = []
    predicted_labels = []
    class_condifences = []
    for ind in range(args.num_folds):
        fold_testset_path = os.path.join(args.kfold_dir, f'fold_{ind}', 'test.tsv')
        fold_test_df = pd.read_csv(fold_testset_path, sep='\t', encoding='utf-8', quoting=3)

        fold_test_labels = [ID_TO_EFFICIENCY_LABEL[label_id] for label_id in fold_test_df.label_id.values]
        fold_test_texts = fold_test_df.text.values
        fold_test_doc_ids = fold_test_df.doc_id.values
        fold_test_sent_ids = fold_test_df.sent_id.values

        doc_ids.extend(fold_test_doc_ids)
        sent_ids.extend(fold_test_sent_ids)
        sentence_texts.extend(fold_test_texts)
        human_labels.extend(fold_test_labels)

        fold_fname = f'fold_{ind}.tsv'
        fold_path = os.path.join(args.classes_folder, fold_fname)
        with codecs.open(fold_path, "r", encoding="utf-8") as fold_file:
            for sent_number, line in enumerate(fold_file):
                class_probabilities = [float(x) for x in line.split()]
                class_id = np.argmax(class_probabilities)
                class_confidence = np.max(class_probabilities)
                predicted_eff_label = ID_TO_EFFICIENCY_LABEL[class_id]
                predicted_labels.append(predicted_eff_label)
                class_condifences.append(class_confidence)

    eff_labels_df = pd.DataFrame.from_dict(
        {'human_label': human_labels, 'predicted_label': predicted_labels, 'class_confidence': class_condifences,
         'doc_id': doc_ids, 'sent_id': sent_ids, 'text': sentence_texts})
    mismatched_labels_df = eff_labels_df[eff_labels_df.human_label != eff_labels_df.predicted_label]
    mismatched_labels_df.reset_index()
    mismatched_labels_df.to_csv(args.save_to, sep='\t', quoting=3, index=False)


if __name__ == '__main__':
    main()
