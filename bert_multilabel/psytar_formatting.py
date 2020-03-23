import os
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split

from PsyTar.merge_psytar import DI_FIILTERED_VALUES

CLASSIFICATION_LABELS = ["INF", "EF", "DI", "ADR", "others"]
PSYTAR_TEXT_COLUMN = ["sentences"]


def main():
    parser = ArgumentParser()
    parser.add_argument("--psytar_dir", required=True)
    parser.add_argument("--n_splits", type=int, default=5)
    parser.add_argument("--output_crossval_dir", required=True)
    args = parser.parse_args()
    psytar_dir = args.psytar_dir

    sent_labeling_csv_path = os.path.join(psytar_dir, 'Sentence_Labeling.csv')
    sent_labeling_df = pd.read_csv(sent_labeling_csv_path, encoding="utf-8")
    sent_labeling_df.drop(sent_labeling_df.tail(1).index, inplace=True)
    sent_labeling_df.loc[sent_labeling_df['DI'].isin(DI_FIILTERED_VALUES), 'DI'] = np.nan
    sent_labeling_df.fillna(0, inplace=True)
    sent_labeling_df[CLASSIFICATION_LABELS] = sent_labeling_df[CLASSIFICATION_LABELS].astype(np.int32)
    sent_labeling_df[CLASSIFICATION_LABELS] = sent_labeling_df[CLASSIFICATION_LABELS].apply(pd.to_numeric)

    kf = KFold(n_splits=args.n_splits)
    for ind, (train_index, test_index) in enumerate(kf.split(sent_labeling_df)):
        print(f"Creating split {ind}")
        print(train_index)
        print(test_index)
        train_df = sent_labeling_df.loc[train_index]
        test_df = sent_labeling_df.loc[test_index]

        fold_directory = os.path.join(args.output_crossval_dir, f'fold_{ind}/')
        if not os.path.exists(fold_directory):
            os.makedirs(fold_directory)
        train_path = os.path.join(fold_directory, 'train.tsv')
        train_df, dev_df, _, _ = train_test_split \
            (train_df, train_df, test_size=0.1, random_state=42)
        dev_path = os.path.join(fold_directory, 'dev.tsv')
        test_path = os.path.join(fold_directory, 'test.tsv')

        train_df.to_csv(train_path)
        test_df.to_csv(test_path)
        dev_df.to_csv(dev_path)


if __name__ == '__main__':
    main()
