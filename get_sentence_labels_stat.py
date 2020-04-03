import os
from argparse import ArgumentParser
from collections import Counter
from sys import stderr

import pandas as pd

SENTENCE_LEVEL_ANNOTATIONS = ['ADR', 'DI', 'Finding', 'EF', 'INF']
RU_CATEGORIES_TO_ENGLISH = {"Снотворные и успокаивающие препараты": "Sleeping",
                            "Иммуномодуляторы": "Immunomodulators",
                            "Антидепрессанты": "Sleeping",
                            "Ноотропные препараты": "Nootropic",
                            "Противовирусные препараты": "Antiviral"}


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_dir', required=True)
    parser.add_argument('--rev_info_csv', required=True)
    parser.add_argument('--output_file', required=True)
    args = parser.parse_args()

    review_info_df = pd.read_csv(args.rev_info_csv, encoding="utf-8", )
    category_annotation_statistics = {}
    counter = Counter()
    for review_folder in os.listdir(args.input_dir):
        processed_review_sentence_ids_set = set()
        review_id = int(review_folder.split('.')[0])
        review_category = review_info_df[review_info_df.id == review_id]['category'].values[0]
        english_cat_name = RU_CATEGORIES_TO_ENGLISH[review_category]
        if category_annotation_statistics.get(english_cat_name) is None:
            counter_dict = {}
            for label in SENTENCE_LEVEL_ANNOTATIONS:
                counter_dict[label] = 0
            category_annotation_statistics[english_cat_name] = counter_dict
        annotation_counter_dict = category_annotation_statistics.get(english_cat_name)

        file_path = os.path.join(args.input_dir, review_folder, 'admin.tsv')
        if not os.path.exists(file_path):
            stderr.write(f"FILE DOES NOT EXIST: {file_path}\n")
            continue
        try:
            annotation_data = pd.read_csv(file_path, sep='\t', skip_blank_lines=True, comment='#', encoding='utf-8',
                                          names=['token_id', 'token_span', 'token', 'entity_id', 'entity_type',
                                                 'unknown_1',
                                                 'efficiency'], usecols=range(7), quoting=3)
            annotation_data['sentence_id'] = annotation_data.token_id.apply(lambda tid: int(tid.split('-')[0]))

            for row in annotation_data.iterrows():
                row_series = row[1]
                efficiency_annotation = row_series['efficiency']
                sentence_id = row_series['sentence_id']
                if sentence_id not in processed_review_sentence_ids_set:
                    flag = False
                    for label in SENTENCE_LEVEL_ANNOTATIONS:
                        if label in efficiency_annotation:
                            flag = True
                            counter[label] += 1
                            annotation_counter_dict[label] += 1
                    if not flag:
                        assert efficiency_annotation == '_'
                    processed_review_sentence_ids_set.add(sentence_id)
        except pd.errors.ParserError as err:
            err_msg = str(err)
            if err_msg == 'Too many columns specified: expected 7 and found 6':
                stderr.write(f'File is not properly annotated: {file_path}\n')
            else:
                stderr.write(f'{err_msg}\n')

    result_df = pd.DataFrame.from_dict(category_annotation_statistics)
    result_df.insert(0, 'Corpus', result_df.sum(axis=1))
    result_df.to_csv(args.output_file, encoding="utf-8", )
    print(result_df)
    print(counter)


if __name__ == '__main__':
    main()
