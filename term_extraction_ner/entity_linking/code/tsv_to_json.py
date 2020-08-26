import codecs
import json
import os
from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_tsv', required=True)
    parser.add_argument('--output_json', required=True)
    args = parser.parse_args()

    input_tsv_path = args.input_tsv
    output_path = args.output_json
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    data_df = pd.read_csv(input_tsv_path, sep='\t')
    data_df.rename(columns={"lemma" : "text"}, inplace=True)
    texts = data_df["text"].values
    records = []
    for text in texts:
        records.append({"text" : text})

    with codecs.open(output_path, 'w+', encoding="utf-8") as output_file:
        output_file.write(
            '[' +
            ',\n'.join(json.dumps(i) for i in records) +
            ']\n')


if __name__ == '__main__':
    main()
