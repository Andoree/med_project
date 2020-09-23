import codecs
import dataclasses
import json

from NLPDatasetIO.dataset import Dataset


def main():
    predicted_test_set = Dataset('../predicted_biobert.txt', 'conll')
    output_filename = 'entities.json'
    num_docs_filename = 'entities_num_docs.txt'
    with codecs.open(output_filename, 'w+', encoding='utf-8') as output_file, \
            codecs.open(num_docs_filename, 'w+', encoding='utf-8') as stats_file:
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
