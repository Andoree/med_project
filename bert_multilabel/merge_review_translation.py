import os

import pandas as pd


def main():
    translation_path = r"otzovik_csvs_translated/fold_0/dev.csv"
    original_data_path = r"otzovik_csvs/fold_0/dev.csv"
    output_dir = r"otzovik_csvs_translated_merged/fold_0/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_fname = r"dev.csv"
    output_path = os.path.join(output_dir, output_fname)

    translation_df = pd.read_csv(translation_path,encoding="utf-8",)
    print('translated\n', translation_df)
    original_data_df = pd.read_csv(original_data_path, encoding="utf-8")
    print('original\n',original_data_df)
    print('translated\n', translation_df.shape)
    print('original\n', original_data_df.shape)
    original_data_df['sentences'] = translation_df['sentences']
    print('original after replace\n', original_data_df)
    original_data_df.to_csv(output_path, index=False, encoding="utf-8")

if __name__ == '__main__':
    main()