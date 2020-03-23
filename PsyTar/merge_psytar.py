import os
from argparse import ArgumentParser

import pandas as pd
import numpy as np

COUNTABLE_LABELS_RANGES = {"ADR": range(1, 31), "WD": range(1, 10), "DI": range(1, 10), "SSI": range(1, 10)}
DI_FIILTERED_VALUES = ["!", "*", "!*", "! "]


def add_label_counter_column(df, label):
    """
    For each row (sentence) adds column with annotated entities count
    :param df: Dataframe of annotated sentences and their entities
    :param label: Annotation label.
    """
    label_index_range = COUNTABLE_LABELS_RANGES[label]
    annotation_col_names = [f"{label}{i}" for i in label_index_range]
    counter_col_name = f'{label.lower()}_count'
    df[counter_col_name] = df.apply(lambda row: row[annotation_col_names].notnull().sum(), axis=1)


def load_annotation_dataframes(psytar_dir, anno_labels):
    """
    Loads dataframes from csv files of sentence annotation. For each
    row (sentence) adds column with annotated entities count
    :param psytar_dir: Directory of PsyTar sentence annotation csvs
    :param anno_labels: List of upper-case annotation labels
    :return: Dataframes with counts of annotated entities in sentences
    """
    dataframes_dict = {}
    for label in anno_labels:
        annotation_csv_path = os.path.join(psytar_dir, f'{label}_Identified.csv')
        annotation_df = pd.read_csv(annotation_csv_path, encoding="utf-8")
        add_label_counter_column(annotation_df, label)
        dataframes_dict[label] = annotation_df
    return dataframes_dict["ADR"], dataframes_dict["WD"], dataframes_dict["DI"], dataframes_dict["SSI"]


def main():
    parser = ArgumentParser()
    parser.add_argument("--save_to_csv", required=True)
    parser.add_argument("--psytar_csvs_dir", required=True)
    args = parser.parse_args()
    psytar_dir = args.psytar_csvs_dir

    sent_labeling_csv_path = os.path.join(psytar_dir, 'Sentence_Labeling.csv')
    sent_labeling_df = pd.read_csv(sent_labeling_csv_path, encoding="utf-8")
    adr_df, wd_df, di_df, ssi_df = load_annotation_dataframes(psytar_dir=psytar_dir,
                                                              anno_labels=COUNTABLE_LABELS_RANGES.keys())
    sent_labeling_df.loc[sent_labeling_df['DI'].isin(DI_FIILTERED_VALUES), 'DI'] = np.nan
    sent_labeling_df["DI"] = pd.to_numeric(sent_labeling_df["DI"])

    resulting_df = sent_labeling_df[
        ["drug_id", "sentence_index", "ADR", "WD", "EF", "INF", "SSI", "DI", "Findings", "others"]]
    resulting_df = resulting_df \
        .merge(adr_df[['drug_id', 'sentence_index', 'adr_count']], how='left', on=['drug_id', 'sentence_index']) \
        .merge(wd_df[['drug_id', 'sentence_index', 'wd_count']], how='left', on=['drug_id', 'sentence_index']) \
        .merge(ssi_df[['drug_id', 'sentence_index', 'ssi_count']], how='left', on=['drug_id', 'sentence_index']) \
        .merge(di_df[['drug_id', 'sentence_index', 'di_count']], how='left', on=['drug_id', 'sentence_index'])

    column_lst = ['adr_count', 'wd_count', 'di_count', 'ssi_count', 'INF', 'EF', 'Findings', ]
    values = {col: 0 for col in column_lst}
    resulting_df.fillna(values, inplace=True)
    resulting_df.drop(resulting_df.tail(1).index, inplace=True)

    adr_stat_df = resulting_df[resulting_df['ADR'] == 1][column_lst].sum().rename("ADR", inplace=True)
    wd_stat_df = resulting_df[resulting_df['WD'] == 1][column_lst].sum().rename("WD", inplace=True)
    di_stat_df = resulting_df[resulting_df['DI'] == 1][column_lst].sum().rename("DI", inplace=True)
    ssi_stat_df = resulting_df[resulting_df['SSI'] == 1][column_lst].sum().rename("SSI", inplace=True)
    ef_stat_df = resulting_df[resulting_df['EF'] == 1][column_lst].sum().rename("EF", inplace=True)
    inf_stat_df = resulting_df[resulting_df['INF'] == 1][column_lst].sum().rename("INF", inplace=True)

    resulting_stat_df = pd.concat([adr_stat_df, wd_stat_df, di_stat_df, ssi_stat_df, ef_stat_df, inf_stat_df],
                                  axis=1, ).transpose()
    resulting_stat_df.index.name = 'Sentence label'
    sentence_labels_stat_df = sent_labeling_df.iloc[-1][['ADR', 'WD', 'DI', 'SSI', 'EF', 'INF']]
    resulting_stat_df.insert(0, 'Sentence count', sentence_labels_stat_df)

    resulting_stat_df = resulting_stat_df.applymap(np.int64)

    resulting_stat_df.to_csv(args.save_to_csv)


if __name__ == '__main__':
    main()
