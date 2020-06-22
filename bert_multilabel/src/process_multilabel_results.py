import os
import sys
from argparse import ArgumentParser

import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report

from bert_multilabel.formatting.otzovik_reviews_formatting import ANNOTATION_LABELS_LIST as labels_list

METRICS = {"Precision": precision_score, "Recall": recall_score,
           "F-score": f1_score, }

def evaluate_classification_results(resulting_df, NUM_LABELS=5, threshold=0.5,
                                    average='binary', pos_label=1):
    predicted_probs_pos_end = resulting_df.shape[1]
    predicted_probs_pos_start = predicted_probs_pos_end - NUM_LABELS
    columns = resulting_df.columns
    labels = columns[1: 1 + NUM_LABELS]
    results_numpy = resulting_df.values.transpose()
    all_true_labels = results_numpy[1: 1 + NUM_LABELS]
    all_pred_probs = results_numpy[predicted_probs_pos_start: predicted_probs_pos_end]
    all_pred_labels = (all_pred_probs >= threshold).astype(int)
    for i in range(NUM_LABELS):
        class_true_labels = all_true_labels[i]
        class_pred_labels = all_pred_labels[i]
        label_name = labels[i]
        print(i, label_name)
        for metric_name, metric in METRICS.items():
            score = metric(y_true=class_true_labels, y_pred=class_pred_labels, labels=labels, )
            print(f"\t{metric_name} : {score}")



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
        label_scores[f"Std {metric_name}"] = 0
        fold_scores = []
        for results_fname in os.listdir(input_dir):
            fold_number = int(results_fname.split('.')[-2].split('_')[-1])
            fold_res_path = os.path.join(input_dir, results_fname)
            fold_results_df = pd.read_csv(fold_res_path, encoding='utf-8')
            true_label_df = fold_results_df[label]

            predicted_label_col_name = f"p_{label}"
            pred_label_df = fold_results_df[predicted_label_col_name].apply(lambda prob: 1 if prob >= 0.5 else 0)
            score = metric(true_label_df, pred_label_df)
            metric_fold_name = f"{metric_name}, fold {fold_number}"
            label_scores[metric_fold_name] = score
            fold_scores.append(score)
        label_scores[f"Avg. {metric_name}"] = np.mean(fold_scores)
        label_scores[f"Std {metric_name}"] = np.std(fold_scores)

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
    overall_statistics = {}

    scores_df = pd.DataFrame.from_dict(folds_results, orient="index", )
    for metric_name in METRICS.keys():
        overall_statistics[f"Avg. {metric_name}"] = scores_df[f"Avg. {metric_name}"].mean()
        overall_statistics[f"Std {metric_name}"] = scores_df[f"Std {metric_name}"].mean()
    overall_stats_df = pd.DataFrame.from_dict({"All": overall_statistics}, orient="index", )
    scores_df = pd.concat((scores_df, overall_stats_df))
    scores_df.index.name = "Label"
    scores_df = scores_df.apply(lambda x: np.round(x, decimals=5), )
    scores_df.to_csv(args.results_file)


if __name__ == '__main__':
    main()
