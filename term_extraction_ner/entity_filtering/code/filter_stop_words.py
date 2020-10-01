from argparse import ArgumentParser
import pandas as pd
from nltk.corpus import stopwords
import nltk
import os


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_path',
                        default=r'../../entity_linking/entities_lemm_vocab_mapping/'
                                'lemm_entities_mappings_with_symbolic_iou_w_stats.tsv')
    parser.add_argument('--column', default='entity')
    parser.add_argument('--output_path',
                        default=r'../filtered_entities/lemm_entities_with_symbolic_iou_w_stats_no_stopwords.tsv')
    args = parser.parse_args()

    input_path = args.input_path
    column_name = args.column
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    entities_df = pd.read_csv(input_path, sep='\t')
    nltk.download("stopwords")
    stop_words_list = set(stopwords.words("russian"))
    print(f"Before filtering: {entities_df.shape[0]} rows")
    entities_df = entities_df[~entities_df[column_name].isin(stop_words_list)]
    print(f"After filtering: {entities_df.shape[0]} rows")
    excluded_df = entities_df[entities_df[column_name].isin(stop_words_list)]
    print("Excluded entities:\n", excluded_df)
    entities_df.to_csv(output_path, '\t', index=False)


if __name__ == '__main__':
    main()
