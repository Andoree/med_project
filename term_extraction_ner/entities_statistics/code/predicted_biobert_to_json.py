import codecs
import dataclasses
import json

from NLPDatasetIO.dataset import Dataset


def main():
    predicted_test_set = Dataset('../predicted_biobert.txt', 'conll')
    output_filename = 'entities.json'
    with codecs.open(output_filename, 'w+', encoding='utf-8') as output_file:
        for document in predicted_test_set.documents:
            doc_dict = {"doc_id": document.doc_id,
                        "doc_text": document.text}
            entities = []
            for entity in document.entities:
                entity_dict = dataclasses.asdict(entity)
                entities.append(entity_dict)
            doc_dict["entities"] = entities
            json.dump(doc_dict, output_file, ensure_ascii=False)
            output_file.write('\n')



if __name__ == '__main__':
    main()
