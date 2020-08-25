import codecs
import os
from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_meddra_path',
                        default=r'/home/tlenusik/DATA/medical_vocabs_and_ontologies/UMLS/UMLS2019AB/full_meddra_vocab.txt')
    parser.add_argument('--output_path', default='meddra_vocab.txt')
    args = parser.parse_args()

    input_meddra_path = args.input_meddra_path
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    meddra_df = pd.read_csv(input_meddra_path, sep='\t')
    meddra_terms_array = meddra_df['STR'].values
    with codecs.open(output_path, 'w+', encoding='utf-8') as output_file:
        for term in meddra_terms_array:
            output_file.write(f"{term.strip()}\n")


if __name__ == '__main__':
    main()
