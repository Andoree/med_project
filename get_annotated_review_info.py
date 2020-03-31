import codecs
import distutils
import json
import os
import re
from argparse import ArgumentParser
from distutils.util import strtobool
from sys import stderr
import pandas as pd

PRODUCT_RATING_PATTERN = r'^Общий рейтинг: (?P<rating_value>\d)$'
PRODUCT_TITLE_PATTERN = r'^Все отзывы о (?P<product_title>.+)$'
IGNORED_CATEGORIES_LIST = ['Гомеопатические препараты']


def get_reviews_ids_set(reviews_directory):
    """
    Returns set of unique review ids from reviews directory.
    :param reviews_directory: Directory of reviews. Contains
    subdirectories of individual reviews.
    :return: set of review ids.
    """
    annotated_reviews_ids = set()
    for review_folder in os.listdir(reviews_directory):
        review_id = int(review_folder.split('.')[0])
        annotated_reviews_ids.add(review_id)
    return annotated_reviews_ids


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
    parser.add_argument('--anno_reviews', required=True)
    parser.add_argument('--save_to', required=True)
    parser.add_argument('--filter_category', type=strtobool, default=False)
    args = parser.parse_args()

    annotated_reviews_ids = get_reviews_ids_set(reviews_directory=args.anno_reviews)
    review_id_lst = []
    category_3_lst = []
    rating_lst = []
    product_name_lst = []

    with codecs.open(args.all_reviews, "r", encoding='utf-8') as inp:
        for line in inp:
            try:
                doc = json.loads(line)
                url = doc['url']
                review_id = int(url.split('/')[-1].split('.')[0].split('_')[-1])
                if review_id not in annotated_reviews_ids:
                    continue
                category_3 = doc['cat3']
                if args.filter_category:
                    if category_3 in IGNORED_CATEGORIES_LIST:
                        continue
                product_rating = get_value_from_list_field(
                    doc, field_name="product-rating", re_pattern=PRODUCT_RATING_PATTERN,
                    re_group_name="rating_value")
                product_title = get_value_from_list_field(
                    doc, field_name="product_name_title", re_pattern=PRODUCT_TITLE_PATTERN,
                    re_group_name="product_title")

                review_id_lst.append(review_id)
                category_3_lst.append(category_3)
                rating_lst.append(product_rating)
                product_name_lst.append(product_title)

            except json.decoder.JSONDecodeError:
                pass
        diff =  annotated_reviews_ids.difference(set(review_id_lst))
        print(f"absent ids:\n{diff}")
        review_data_df = pd.DataFrame.from_dict({"id": review_id_lst, "category": category_3_lst,
                                                 "rating": rating_lst, "product_name": product_name_lst})
        review_data_df.to_csv(args.save_to, encoding="utf-8", index=False)


if __name__ == '__main__':
    main()
