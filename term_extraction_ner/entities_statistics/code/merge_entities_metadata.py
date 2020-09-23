import codecs
import dataclasses
import json
import os
from argparse import ArgumentParser
from typing import Dict

from NLPDatasetIO.dataset import Dataset

FILENAME_TO_COLLECTION_NAME = {
    "all_reviews_texts.txt": "otzovik",
    "comments.json": "comments",
    "consumers_drugs_reviews.json": "consumers",
    "doctors_drugs_reviews.json": "doctors",
    "spr-ru.txt": "spr"
}


def append_source_to_sentence(sentence_json: Dict, sentence_metadata_json: Dict):
    """
    Appends source url and, if it is present, source review
    id to the sentence dictionary. Modifies the existing sentence_json
    Dict.
    :param sentence_json:
    :param sentence_metadata_json:
    """
    metadata_filename = sentence_metadata_json["filename"]
    del sentence_json["filename"]
    sentence_json["source"] = FILENAME_TO_COLLECTION_NAME[metadata_filename]

    if metadata_filename == "all_reviews_texts.txt":
        sentence_json["url"] = sentence_metadata_json["url"]
    elif metadata_filename == "comments":
        sentence_json["url"] = sentence_metadata_json["url"]
        sentence_json["review_id"] = sentence_metadata_json["url"]
    elif metadata_filename == "consumers_drugs_reviews.json" or metadata_filename == "doctors_drugs_reviews.json":
        sentence_json["url"] = sentence_metadata_json["url"]
    elif metadata_filename == "spr-ru.txt":
        sentence_json["url"] = sentence_metadata_json.get("url")
        sentence_json["id"] = sentence_metadata_json.get("review_id")
    else:
        raise ValueError("Invalid metadata filename")

    del sentence_json["filename"]
    sentence_json["source"] = FILENAME_TO_COLLECTION_NAME[metadata_filename]


def main():
    parser = ArgumentParser()
    parser.add_argument('--entities_path', default='../../rudrec_markup/predicted_biobert.txt')
    parser.add_argument('--metadata_path', default=r'../../rudrec_markup/rudrec_sentences_metadata.json')
    parser.add_argument('--output_path', default='../../rudrec_markup/entities_with_metadata.json')
    args = parser.parse_args()

    entities_path = args.entities_path
    metadata_path = args.metadata_path
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    with codecs.open(entities_path, 'r', encoding="utf-8") as entities_file, \
            codecs.open(metadata_path, 'r', encoding="utf-8") as metadata_file, \
            codecs.open(output_path, 'w+', encoding="utf-8") as output_file:
        metadata_pointer = -1
        for line in entities_file:
            line = line.strip()
            sentence_json = json.loads(line)
            sentence_id = int(sentence_json)
            while metadata_pointer < sentence_id:
                metadata_line = metadata_file.readline()
                metadata_pointer += 1
            if metadata_pointer == sentence_id:
                metadata_line = metadata_line.strip()
                sentence_metadata_json = json.loads(metadata_line)
                append_source_to_sentence(sentence_json, sentence_metadata_json)
                json.dump(sentence_json, output_file, ensure_ascii=False)
                output_file.write("\n")


if __name__ == '__main__':
    main()
