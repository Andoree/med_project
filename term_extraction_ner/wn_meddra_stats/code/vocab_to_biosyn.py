import os
from argparse import ArgumentParser
import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--vocab_path',
                        default=r'../wordnet_meddra/wn_pt_lltmeddra_intersection/pt_llt_wordnet_lemm_meddra_intersection.tsv')
    # default=r'../vocabs/vocabs_w_metadata/pt_llt_lemmatized_ru_meddra_vocab.tsv')
    parser.add_argument('--keep_columns', nargs='+', default=["term", "umls_cui"])
    parser.add_argument('--minus_one_columns', type=int, nargs='+', default=[0, 2, 3, 5])
    parser.add_argument('--none_columns', type=int, nargs='+', default=[1, 4, 6, 8])
    parser.add_argument('--output_path',
                        default=r'../wordnet_meddra/meddra_biosyn/wn_meddra_intersection_biosyn_filtered.tsv')
    args = parser.parse_args()

    vocab_path = args.vocab_path
    keep_columns_list = args.keep_columns
    minus_one_columns_ids_list = args.minus_one_columns
    none_columns_ids_list = args.none_columns
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    columns = []
    assert len(set(minus_one_columns_ids_list).intersection(set(none_columns_ids_list))) == 0
    for minus_one_col_id in minus_one_columns_ids_list:
        columns.append((minus_one_col_id, -1))
    for none_col_id in none_columns_ids_list:
        columns.append((none_col_id, ''))
    columns.sort(key=lambda t: t[0])

    vocab_df = pd.read_csv(vocab_path, sep='\t', encoding="utf-8")
    output_df = vocab_df[keep_columns_list].copy()
    num_rows = vocab_df.shape[0]
    for (col_id, value) in columns:
        values_list = [value for i in range(num_rows)]
        values_df = pd.Series(values_list)
        output_df.insert(col_id, col_id, values_df)
    output_df.drop_duplicates(inplace=True)
    print(output_df.shape[0])
    print(len(output_df.umls_cui.unique()))
    output_df.to_csv(output_path, sep='|', encoding="utf-8", index=False)


if __name__ == '__main__':
    main()
