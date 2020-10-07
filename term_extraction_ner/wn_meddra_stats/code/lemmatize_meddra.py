import os
from argparse import ArgumentParser

import pandas as pd

from lemmatize_entities import load_pipeline, process_udpipe
from term_extraction_ner.entities_statistics.code.lemmatize_entities import unify_sym


def main():
    parser = ArgumentParser()
    parser.add_argument('--meddra_path',
                        default=r'../vocabs/vocabs_w_metadata/ru_meddra_vocab.tsv')
    parser.add_argument('--output_path', default=r'../vocabs/vocabs_w_metadata/lemmatized_ru_meddra_vocab.tsv')
    args = parser.parse_args()

    meddra_path = args.meddra_path
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    process_pipeline, model = load_pipeline()
    print('Model is loaded. Starting lemmatization')
    meddra_df = pd.read_csv(meddra_path, sep='\t', encoding="utf-8")
    meddra_df["lemm_term"] = meddra_df["term"].apply(
        lambda x: ' '.join(process_udpipe(process_pipeline, text=unify_sym(x), keep_pos=False)))


if __name__ == '__main__':
    main()
