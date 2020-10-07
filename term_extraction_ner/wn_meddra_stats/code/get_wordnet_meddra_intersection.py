import os
from argparse import ArgumentParser
import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--wordnet_path',
                        default=r'../wordnet_meddra/wordnet_med_senses_synsets.tsv')
    parser.add_argument('--meddra_path',
                        default=r'../vocabs/vocabs_w_metadata/ru_meddra_vocab.tsv')
    parser.add_argument('--output_path', default=r'../wordnet_meddra/wordnet_meddra_intersection.tsv')
    args = parser.parse_args()

    wordnet_path = args.wordnet_path
    meddra_path = args.meddra_path
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and output_dir != '':
        os.makedirs(output_dir)

    wordnet_df = pd.read_csv(wordnet_path, sep='\t', encoding="utf-8")
    meddra_df = pd.read_csv(meddra_path, sep='\t', encoding="utf-8")
    print(f"Wordnet size: {wordnet_df.shape[0]}")
    print(f"Meddra size: {meddra_df.shape[0]}")
    wordnet_df["sense_term"] = wordnet_df["sense_term"].apply(lambda x: x.lower())
    meddra_df["term"] = meddra_df["term"].apply(lambda x: x.lower())

    joined_df = pd.merge(wordnet_df, meddra_df, left_on="sense_term", right_on="term", how="inner", )
    print(f"Intersection size: {joined_df.shape[0]}")
    joined_df.to_csv(output_path, sep='\t', encoding="utf-8", index=False)


if __name__ == '__main__':
    main()
