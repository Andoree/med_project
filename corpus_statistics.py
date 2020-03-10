import codecs
import json
from collections import Counter


def main():
    with codecs.open("annotated_reviews.json", "r", encoding="utf-8") as json_input:
        data = json.load(json_input)
        counter = Counter()
        for sentence in data:
            efficiency_label = sentence['type']
            counter[efficiency_label] += 1
        for tag, freq in counter.items():
            print(tag, freq)


if __name__ == '__main__':
    main()
