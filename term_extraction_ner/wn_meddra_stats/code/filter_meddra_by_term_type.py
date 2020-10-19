import os
from argparse import ArgumentParser
import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--meddra_path',
                        default=r'../vocabs/vocabs_w_metadata/lemmatized_ru_meddra_vocab.tsv')
    parser.add_argument('--keep_types', nargs='+', default=["PT", "LLT"])
    parser.add_argument('--output_path',
                        default=r'../vocabs/vocabs_w_metadata/pt_llt_lemmatized_ru_meddra_vocab.tsv')
    args = parser.parse_args()

    input_meddra_path = args.meddra_path
    keep_types_list = args.keep_types
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    meddra_df = pd.read_csv(input_meddra_path, sep='\t', encoding="utf-8")
    print(f"Meddra vocab size: {meddra_df.shape[0]}")
    filtered_meddra = meddra_df[meddra_df.term_type.isin(keep_types_list)]
    print(f"Meddra vocab size: {filtered_meddra.shape[0]}")
    filtered_meddra.to_csv(output_path, sep='\t', encoding="utf-8", index=False)


if __name__ == '__main__':
    main()
