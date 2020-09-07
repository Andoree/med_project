import os
from argparse import ArgumentParser
from typing import List

import pandas as pd

from term_extraction_ner.entities_statistics.code.lemmatize_entities import list_replace
from term_extraction_ner.entity_linking.code.iou.symbolic_trigram_iou import calculate_symbolic_trigram_iou

from term_extraction_ner.entity_linking.code.iou.iou_utils import token_words_iou_metric, calculate_row_columns_iou


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


IOU_TYPES = {
    'symbolic': calculate_symbolic_trigram_iou,
    'word': token_words_iou_metric
}


def main():
    # todo: probably, stemming
    parser = ArgumentParser()
    parser.add_argument('--input_path', )
    parser.add_argument('--vocab_paths', nargs='+')
    parser.add_argument('--lemm_vocab_paths', nargs='+')
    parser.add_argument('--entity_column', )
    parser.add_argument('--vocab_columns', nargs='+')
    parser.add_argument('--iou_type', choices=IOU_TYPES.keys())
    parser.add_argument('--output_path')
    args = parser.parse_args()

    input_path = args.input_path
    vocab_paths = args.vocab_paths
    lemm_vocab_paths = args.lemm_vocab_paths
    entity_column = args.entity_column
    vocab_columns = args.vocab_columns
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and output_dir != '':
        os.makedirs(output_dir)
    iou_metric = IOU_TYPES[args.iou_type]
    assert len(vocab_paths) == len(lemm_vocab_paths)
    assert len(lemm_vocab_paths) == len(vocab_columns)
    assert len(vocab_columns) == len(vocab_paths)

    entity_vocab_mapping_df = pd.read_csv(input_path, sep='\t')
    for i in range(len(vocab_paths)):
        vocab_path = vocab_paths[i]
        lemm_vocab_path = lemm_vocab_paths[i]
        vocab_column = vocab_columns[i]
        vocab_df = pd.read_csv(vocab_path, sep='\t', header=None, names=['id', 'concept'])
        vocab_df.concept = vocab_df.concept.apply(lambda x: list_replace(search='"', replacement='', text=x))
        vocab_df.concept = vocab_df.concept.apply(lambda x: x.strip())
        vocab_list = vocab_df.concept.values
        lemm_vocab_df = pd.read_csv(lemm_vocab_path, sep='\t', header=None, names=['id', 'concept'])
        lemm_vocab_list = lemm_vocab_df.concept.values
        assert len(vocab_list) == len(lemm_vocab_list)
        vocab_to_lemm_dict = {vocab_list[i]: lemm_vocab_list[i]
                              for i in range(len(vocab_list))}
        iou_column_name = f'{entity_column}_{vocab_column}_iou'
        entity_vocab_mapping_df[iou_column_name] = entity_vocab_mapping_df.apply(
            lambda row: calculate_row_columns_iou(row, entity_column=entity_column, iou_metric=iou_metric,
                                                  vocab_column=vocab_column, vocab_to_lemm_dict=vocab_to_lemm_dict),
            axis=1)
        entity_vocab_mapping_df.to_csv(output_path, sep='\t', index=False)


if __name__ == '__main__':
    main()
