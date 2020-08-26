import codecs
import os
from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_tsv',
                        default=r'/home/tlenusik/DATA/medical_vocabs_and_ontologies/UMLS/UMLS2019AB/full_meddra_vocab.txt')
    parser.add_argument('--output_path', default='meddra_vocab.txt')
    parser.add_argument('--text_column', required=True)
    args = parser.parse_args()

    input_tsv_path = args.input_tsv
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    text_column_name = args.text_column

    id_concept_df = pd.read_csv(input_tsv_path, sep='\t')
    vocab_terms_array = id_concept_df[text_column_name].values
    with codecs.open(output_path, 'w+', encoding='utf-8') as output_file:
        for term in vocab_terms_array:
            output_file.write(f"{term.strip()}\n")


if __name__ == '__main__':
    main()
