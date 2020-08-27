import codecs
import os
from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_tsv_1', )
    parser.add_argument('--input_tsv_2', )
    parser.add_argument('--output_path', )
    parser.add_argument('--join_column', required=True)
    args = parser.parse_args()

    input_tsv_1 = args.input_tsv_1
    input_tsv_2 = args.input_tsv_2
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    join_column = args.join_column

    data_df_1 = pd.read_csv(input_tsv_1, sep='\t', )
    data_df_2 = pd.read_csv(input_tsv_2, sep='\t', )
    merged_df = data_df_1.join(data_df_2, how='inner', on=join_column)
    merged_df.to_csv(output_path, sep='\t')


if __name__ == '__main__':
    main()
