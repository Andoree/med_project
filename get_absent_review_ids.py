import codecs
import json
from argparse import ArgumentParser

import pandas as pd

def main():
    parser = ArgumentParser()
    parser.add_argument('--review_info', required=True)
    parser.add_argument('--sent_json', required=True)
    args = parser.parse_args()

    json_review_ids = set()
    with codecs.open(args.sent_json, "r", encoding='utf-8') as inp:
        doc = json.loads(inp.read())
        for review in doc:
            json_review_ids.add(int(review["id"]))
    csv_df = pd.read_csv(args.review_info, encoding='utf-8', )
    csv_ids = set(csv_df.id.values)
    delta = json_review_ids.difference(csv_ids)
    print(delta)

if __name__ == '__main__':
    main()
