import codecs
import json
import os
from argparse import ArgumentParser
import pandas as pd
from sklearn.model_selection import train_test_split

from get_annotated_review_info import get_value_from_list_field, PRODUCT_RATING_PATTERN
from otzovik_preprocessing.crossval_corpus_split import EFFICIENCY_LABEL_TO_ID

RATING_TO_LABEL = {"1": "INF", "3": "NEUTRAL", "5": "EF"}


def main():
    parser = ArgumentParser()
    parser.add_argument('--all_reviews', required=True)
    parser.add_argument('--save_to', required=True)
    parser.add_argument('--max_docs_per_label', type=int, default=10000)
    args = parser.parse_args()

    output_dir = args.save_to
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    all_reviews = []
    counters = {"1": 0, "3": 0, "5": 0}
    max_docs_per_label = args.max_docs_per_label
    with codecs.open(args.all_reviews, "r", encoding='utf-8') as inp:
        for line in inp:
            try:
                doc = json.loads(line)
                review_text = doc['description']
                product_rating = get_value_from_list_field(
                    doc, field_name="product-rating", re_pattern=PRODUCT_RATING_PATTERN,
                    re_group_name="rating_value")
                product_label = RATING_TO_LABEL.get(product_rating)

                if product_label is not None and counters[product_rating] < max_docs_per_label:
                    label_id = EFFICIENCY_LABEL_TO_ID[product_label]
                    review_dict = {
                        "label_id": label_id,
                        "sentences": review_text
                    }
                    all_reviews.append(review_dict)
                    counters[product_rating] += 1
            except json.decoder.JSONDecodeError:
                pass

        data_df = pd.DataFrame(all_reviews)
        print(data_df)
        train_df, dev_df, _, _ = \
            train_test_split(data_df, data_df, test_size=0.1, random_state=42)
        train_path = os.path.join(output_dir, 'train.tsv')
        dev_path = os.path.join(output_dir, 'dev.tsv')

        train_df.to_csv(train_path, index=False, sep="\t")
        dev_df.to_csv(dev_path, index=False, sep="\t")


if __name__ == '__main__':
    main()
