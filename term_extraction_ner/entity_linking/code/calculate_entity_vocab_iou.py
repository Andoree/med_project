import codecs
import os
from argparse import ArgumentParser
from typing import List

import pandas as pd


def strip_list(token: str, strip_tokens: List[str]):
    """
    :param token: Token to get applied strip
    :param strip_tokens: List of strip tokens. There tokens are
    in the same ordet they are in the list.
    :return: Stripped token
    """
    for strip_t in strip_tokens:
        token = token.strip(strip_t)
    return token


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
    iou_score = pairwise_iou_metric(entity_token.split(), lemm_vocab_token.split())
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
    vocab_df = pd.read_csv(vocab_path, sep='\t', header=None, names=['id', 'concept'])
    vocab_df.concept = vocab_df.concept.apply(lambda x: strip_list(x, ['"', ' ']))
    vocab_list = vocab_df.concept.values
    lemm_vocab_df = pd.read_csv(lemm_vocab_path, sep='\t', header=None, names=['id', 'concept'])
    lemm_vocab_list = lemm_vocab_df.concept.values
    assert len(vocab_list) == len(lemm_vocab_list)
    #print(len(vocab_list))
    #print(len(lemm_vocab_list))
    #print(vocab_list[:10])
    #print(lemm_vocab_list[:10])
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
