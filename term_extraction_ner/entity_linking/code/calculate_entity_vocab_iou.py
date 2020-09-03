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


def calculate_row_columns_iou(row, entity_column,
                              vocab_column, vocab_to_lemm_dict):
    """
    :param row: Pandas.Series
    :return: IoU score for the values of two columns listed
    in <column_names> of dataframe's <row>
    """
    entity_token = row[entity_column]
    vocab_token = row[vocab_column]
    lemm_vocab_token = vocab_to_lemm_dict[vocab_token]
    iou_score = pairwise_iou_metric(entity_token, lemm_vocab_token)
    return iou_score


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_path', )
    parser.add_argument('--vocab_path')
    parser.add_argument('--lemm_vocab_path')
    parser.add_argument('--entity_column', )
    parser.add_argument('--vocab_column', )
    parser.add_argument('--output_path')
    args = parser.parse_args()

    input_path = args.input_path
    vocab_path = args.vocab_path
    lemm_vocab_path = args.lemm_vocab_path
    entity_column = args.entity_column
    vocab_column = args.vocab_column
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and output_dir != '':
        os.makedirs(output_dir)
    vocab_list = []
    with codecs.open(vocab_path, 'w', encoding='utf-8') as inp_file:
        for line in inp_file:
            token = line.split()[1].strip()
            vocab_list.append(token)
    lemm_vocab_list = []
    with codecs.open(lemm_vocab_path, 'w', encoding='utf-8') as inp_file:
        for line in inp_file:
            token = line.split()[1].strip()
            lemm_vocab_list.append(token)
    assert len(vocab_list) == len(lemm_vocab_list)
    vocab_to_lemm_dict = {vocab_list[i]: lemm_vocab_list[i]
                          for i in range(len(vocab_list))}

    entity_vocab_mapping_df = pd.read_csv(input_path, sep='\t')
    iou_column_name = f'{entity_column}_{vocab_column}_iou'
    entity_vocab_mapping_df[iou_column_name] = entity_vocab_mapping_df.apply(
        lambda row: calculate_row_columns_iou(row, entity_column=entity_column,
                                              vocab_column=vocab_column, vocab_to_lemm_dict=vocab_to_lemm_dict), axis=1)
    entity_vocab_mapping_df.to_csv(output_path, sep='\t', index=False)


if __name__ == '__main__':
    main()
