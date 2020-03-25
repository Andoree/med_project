import os
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split

from PsyTar.psytar_statistics import DI_FIILTERED_VALUES

CLASSIFICATION_LABELS = ["EF", "INF", "ADR", "DI", "others"]
DATAFRAME_COLUMNS = ["sentences", "EF", "INF", "ADR", "DI", "others", "drug_id", "sentence_index"]


def main():
    parser = ArgumentParser()
    parser.add_argument("--psytar_dir", required=True)
    parser.add_argument("--n_splits", type=int, default=5)
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()
    psytar_dir = args.psytar_dir
    output_dir = args.output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sent_labeling_csv_path = os.path.join(psytar_dir, 'Sentence_Labeling.csv')
    sent_labeling_df = pd.read_csv(sent_labeling_csv_path, encoding="utf-8")
    sent_labeling_df.drop(sent_labeling_df.tail(1).index, inplace=True)
    sent_labeling_df.loc[sent_labeling_df['DI'].isin(DI_FIILTERED_VALUES), 'DI'] = np.nan
    sent_labeling_df.fillna(0, inplace=True)
    sent_labeling_df[CLASSIFICATION_LABELS] = sent_labeling_df[CLASSIFICATION_LABELS].astype(np.int32)
    sent_labeling_df[CLASSIFICATION_LABELS] = sent_labeling_df[CLASSIFICATION_LABELS].apply(pd.to_numeric)
    sent_labeling_df = sent_labeling_df[DATAFRAME_COLUMNS]
    train_df, test_df, _, _ = train_test_split \
        (sent_labeling_df, sent_labeling_df, test_size=0.2, random_state=42)
    train_df, dev_df, _, _ = train_test_split \
        (train_df, train_df, test_size=0.1, random_state=42)

    train_path = os.path.join(output_dir, 'train.csv')
    dev_path = os.path.join(output_dir, 'dev.csv')
    test_path = os.path.join(output_dir, 'test.csv')
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    dev_df.to_csv(dev_path, index=False)


if __name__ == '__main__':
    main()
