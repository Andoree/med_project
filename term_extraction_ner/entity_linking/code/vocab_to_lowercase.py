import codecs
import json
import os
from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_tsv', required=True)
    parser.add_argument('--output_path', required=True)
    args = parser.parse_args()

    input_tsv_path = args.input_tsv
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    data_df = pd.read_csv(input_tsv_path, sep='\t', header=None, names=['id', 'text'])
    data_df['text'] = data_df['text'].apply(lambda x: x.lower())

    data_df.to_csv(output_path, sep='\t', index=False, header=None)


if __name__ == '__main__':
    main()
