import codecs
import json
import os
import re
from argparse import ArgumentParser
from sys import stderr
from collections import Counter
import pandas as pd
from sklearn.model_selection import train_test_split

PRODUCT_RATING_PATTERN = r'^Общий рейтинг: (?P<rating_value>\d)$'
EFFICIENCY_LABEL_TO_ID = {
    "NEUTRAL": 0,
    "EF": 1,
    "INF": 2
}
RATING_TO_LABEL = {"1": "INF", "3": "NEUTRAL", "5": "EF"}

def get_value_from_list_field(json_object_dict, field_name, re_pattern, re_group_name, ):
    """
    :param json_object_dict: dictionary of object (review) fields
    :param field_name: dictionary of review attributes
    :param re_pattern: regex pattern for field value
    :param re_group_name: regex group name of extracted value
    :return: str: field value
    """
    field_value_list = json_object_dict[field_name]
    assert type(field_value_list) == list
    field_value = ''
    if len(field_value_list) > 0:
        field_string = field_value_list[0].strip()
        rating_match = re.fullmatch(re_pattern, field_string)
        if rating_match is not None:
            field_value = rating_match.group(re_group_name)
        else:
            stderr.write(f'INVALID RATING STRING: {field_string}\n')
    return field_value



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
    # max_docs_per_label = args.max_docs_per_label
    counter = Counter()
    with codecs.open(args.all_reviews, "r", encoding='utf-8') as inp:
        for line in inp:
            try:
                doc = json.loads(line)
                review_text = doc['description'].replace("\n", " ")
                product_rating = get_value_from_list_field(
                    doc, field_name="product-rating", re_pattern=PRODUCT_RATING_PATTERN,
                    re_group_name="rating_value")
                if product_rating in counters.keys() and not len(review_text) < 5:
                    counter[product_rating] += 1
                
            except json.decoder.JSONDecodeError:
                pass
    max_docs_per_label = min(counter.values())
    print(max_docs_per_label)
    counters = {"1": 0, "3": 0, "5": 0}
    with codecs.open(args.all_reviews, "r", encoding='utf-8') as inp:
        for line in inp:
            try:
                doc = json.loads(line)
                review_text = doc['description'].replace("\n", " ")
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
                    if len(review_text) < 5:
                        print(review_text)
                    else:
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

        train_df.to_csv(train_path,index=False, header=False, sep="\t", quoting=3)
        dev_df.to_csv(dev_path, index=False, header=False, sep="\t", quoting=3)


if __name__ == '__main__':
    main()
