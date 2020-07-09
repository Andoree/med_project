import os

import pandas as pd


def main():
    input_csv_path = r"../otzovik_csvs/fold_4/dev.csv"
    output_dir = r'../otzovik_csvs_texts/fold_4'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_fname = 'dev.csv'
    output_path = os.path.join(output_dir, output_fname)
    reviews_df = pd.read_csv(input_csv_path, encoding="utf-8")
    review_texts_df = reviews_df['sentences']
    review_texts_df.to_csv(output_path, index=False)


if __name__ == '__main__':
    main()
