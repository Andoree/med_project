import codecs
import os
from argparse import ArgumentParser
from typing import List

import pandas as pd


def pairwise_iou_metric(data_1: List, data_2: List):
    """
    Calculates intersection over union (IoU) for two data lists.
    Data types of the elements of two lists should be the same.
    :return: iou value for the 2 given datasets
    """
    data_1 = set(data_1)
    data_2 = set(data_2)
    intersection = data_1.intersection(data_2)
    union = data_1.union(data_2)
    iou_value = len(intersection) / len(union)
    return iou_value


def calculate_row_columns_iou(row, column_names):
    """
    :param row: Pandas.Series
    :param column_names: List of two column names for which
    the function calculates IoU value.
    :return: IoU score for the values of two columns listed
    in <column_names> of dataframe's <row>
    """
    values = []
    for column_name in column_names:
        cell_value = row[column_name]
        values.append(cell_value.split())
    data_1 = values[0]
    data_2 = values[1]
    iou_score = pairwise_iou_metric(data_1, data_2)
    return iou_score


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_path', )
    parser.add_argument('--input_columns', nargs='+')
    parser.add_argument('--output_path')
    args = parser.parse_args()

    input_path = args.input_path
    columns_list = args.columns
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and output_dir != '':
        os.makedirs(output_dir)
    if len(columns_list) > 2 or len(columns_list == 0):
        raise ValueError(f"Can only calculate IoU of 2 columns, {len(columns_list)} were given")

    entity_vocab_mapping_df = pd.read_csv(input_path, sep='\t')
    iou_column_name = f'{"_".join(columns_list)}_iou'
    entity_vocab_mapping_df[iou_column_name] = entity_vocab_mapping_df.apply(
        lambda row: calculate_row_columns_iou(row, columns_list), axis=1)
    entity_vocab_mapping_df.to_csv(output_path, sep='\t', index=False)


if __name__ == '__main__':
    main()
