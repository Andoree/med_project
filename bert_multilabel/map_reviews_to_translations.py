import os
import pandas as pd


def main():
    id_eng_text_mapping_csv_path = r"otzovik_csvs_translated_merged/all_reviews.csv"
    output_dir = r"otzovik_csvs_translated_merged/fold_4"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_fname = r"test.csv"
    output_path = os.path.join(output_dir, output_fname)
    reviews_path = r"otzovik_csvs/fold_4/test.csv"

    id_eng_text_df = pd.read_csv(id_eng_text_mapping_csv_path, encoding="utf-8")
    id_eng_text_df.rename(inplace=True, columns={"sentences": "eng_sentences"})
    id_eng_text_df = id_eng_text_df[["review_id", "sentence_id", "eng_sentences"]]
    reviews_df = pd.read_csv(reviews_path, encoding="utf-8")
    print("original_data before merge\n", reviews_df)

    joined_df = pd.merge(reviews_df, id_eng_text_df, how='inner', left_on=["review_id", "sentence_id"],
                         right_on=["review_id", "sentence_id"])
    joined_df['sentences'] = joined_df['eng_sentences']
    joined_df.drop(columns=['eng_sentences'],inplace=True)
    print("Joined df\n", joined_df)
    joined_df.to_csv(output_path, index=False)

if __name__ == '__main__':
    main()
