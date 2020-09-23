import codecs
import dataclasses
import json
import os
from argparse import ArgumentParser

from NLPDatasetIO.dataset import Dataset


def main():
    parser = ArgumentParser()
    parser.add_argument('--predicted_path', default='../../rudrec_markup/predicted_biobert.txt')
    parser.add_argument('--output_path', default=r'entities.json')
    parser.add_argument('--output_num_docs', default='entities_num_docs.txt')
    args = parser.parse_args()

    predicted_path = args.predicted_path
    output_num_docs_path = args.output_num_docs
    output_dir = os.path.dirname(output_num_docs_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    predicted_test_set = Dataset(predicted_path, 'conll')

    with codecs.open(output_path, 'w+', encoding='utf-8') as output_file, \
            codecs.open(output_num_docs_path, 'w+', encoding='utf-8') as stats_file:
        for document in predicted_test_set.documents:
            doc_dict = {"sent_id": document.doc_id,
                        "sent_text": document.text}
            entities = []
            for entity in document.entities:
                entity_dict = dataclasses.asdict(entity)
                del entity_dict["label"]
                entities.append(entity_dict)
            doc_dict["entities"] = entities
            if len(entities) > 0:
                json.dump(doc_dict, output_file, ensure_ascii=False)
                output_file.write('\n')
        stats_file.write(f"Num sentences: {len(predicted_test_set.documents)}\n")


if __name__ == '__main__':
    main()
