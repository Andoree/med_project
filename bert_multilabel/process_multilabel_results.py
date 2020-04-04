import os
from argparse import ArgumentParser

import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

from bert_multilabel.formatting.otzovik_reviews_formatting import ANNOTATION_LABELS_LIST as labels_list

METRICS = {"Precision": precision_score, "Recall": recall_score,
           "F-score": f1_score, }


def get_label_scores(input_dir, label):
    """
    :param input_dir: Directory containing results of
    k-folds multilabel classification.
    :param label: Quality metrics will be calculated for
    this classification label.
    :return: Dictionary {"Metric_name, fold_number" : score}
    """
    label_scores = {}
    for metric_name, metric in METRICS.items():
        label_scores[f"Avg. {metric_name}"] = 0
        fold_scores = []
        for results_fname in os.listdir(input_dir):
            fold_number = int(results_fname.split('.')[-2][-1])
            fold_res_path = os.path.join(input_dir, results_fname)
            results_df = pd.read_csv(fold_res_path, encoding='utf-8')
            true_label_df = results_df[label]
            predicted_label_col_name = f"p_{label}"
            pred_label_df = results_df[predicted_label_col_name].apply(lambda prob: 1 if prob >= 0.5 else 0)
            score = metric(true_label_df, pred_label_df)
            metric_fold_name = f"{metric_name}, fold {fold_number}"
            label_scores[metric_fold_name] = np.round(score, decimals=3)
            fold_scores.append(score)
        label_scores[f"Avg. {metric_name}"] = np.round(np.mean(fold_scores), decimals=3)
    return label_scores


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_dir', required=True)
    parser.add_argument('--results_file', required=True)
    args = parser.parse_args()

    input_dir = args.input_dir
    folds_results = {}

    for label in labels_list:
        label_scores = get_label_scores(input_dir=input_dir, label=label)
        folds_results[label] = label_scores
    scores_df = pd.DataFrame.from_dict(folds_results, orient="index", )
    scores_df.index.name = "Label"
    scores_df.to_csv(args.results_file)


if __name__ == '__main__':
    main()
