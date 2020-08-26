import codecs
import os
from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_tsv', required=True)
    parser.add_argument('--output_path', required=True)
    parser.add_argument('--keep_columns', nargs='+', required=True)
    parser.add_argument('--keep_header', action='store_true')
    args = parser.parse_args()

    input_tsv_path = args.input_tsv
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    keep_columns = args.keep_columns
    keep_header = args.keep_header

    data_df = pd.read_csv(input_tsv_path, sep='\t')
    data_df = data_df[keep_columns]
    data_df.to_csv(output_path, sep='\t', index=False, header=keep_header)


if __name__ == '__main__':
    main()
