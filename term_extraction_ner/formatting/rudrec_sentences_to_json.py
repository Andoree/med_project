import ast
import codecs
import json
import os
from argparse import ArgumentParser
from json import JSONDecodeError

from nltk import sent_tokenize
from rudrec_to_conll import clean_text, TEXT_COLUMNS, PROCESS_AS_JSON_DOC


def get_rudrec_doc_id(doc, filename, doc_id):
    if filename == "all_reviews_texts.txt":
        doc_url = doc["url"]
        new_doc_id = doc_url.split('/')[-1].split('.')[0].split('_')[-1]
        new_doc_id = f"otz_{new_doc_id}"
        old_doc_id = new_doc_id
    elif filename == "comments.json":
        new_doc_id = doc["id"]
        new_doc_id = f"com_{new_doc_id}"
        old_doc_id = new_doc_id
    elif filename == "consumers_drugs_reviews.json":
        old_doc_id = doc["url"]
        new_doc_id = f"con_{doc_id}"
    elif filename == "doctors_drugs_reviews.json":
        old_doc_id = doc["url"]
        new_doc_id = f"doc_{doc_id}"
    elif filename == "spr-ru.txt":
        new_doc_id = doc.get("review_id")
        if new_doc_id is None:
            old_doc_id = doc.get("url")
            if old_doc_id is None:
                old_doc_id = f"spr_-{doc_id}"
            new_doc_id = f"spr_-{doc_id}"
        else:
            old_doc_id = new_doc_id
            new_doc_id = f"spr_{new_doc_id}"
    else:
        raise Exception("Invalid filename in get_rudrec_doc_id function")

    assert '\t' not in new_doc_id
    assert '\t' not in old_doc_id
    return old_doc_id, new_doc_id


def fulldoc_to_json(input_file, filename, output_file, map_file, global_id):
    file_text = input_file.read()
    docs = json.loads(file_text)
    for i, doc in enumerate(docs):
        for text_field in TEXT_COLUMNS[filename]:
            document_text = doc[text_field]
            if document_text is not None:
                preprocessed_text = clean_text(document_text)
                preprocessed_text = preprocessed_text.strip()
                old_doc_id, new_doc_id = get_rudrec_doc_id(doc, filename, doc_id=i)
                sentenized_text = sent_tokenize(preprocessed_text, language='russian')

                if len(sentenized_text) > 0:
                    for sentence_id, sentence in enumerate(sentenized_text):
                        global_id += 1
                        sentence = sentence.replace('\n', ' ')
                        if new_doc_id is not None:
                            if old_doc_id != new_doc_id:
                                map_file.write(f"{old_doc_id}\t{new_doc_id}\n")
                            json_entry = {
                                "doc_id": new_doc_id,
                                "sentence_id": sentence_id,
                                "text": sentence,
                            }
                            json.dump(json_entry, output_file, ensure_ascii=False)
                            output_file.write("\n")
    return global_id

def jsondoc_linewise_to_json(input_file, filename, output_file, map_file, global_id):
    for i, line in enumerate(input_file):
        try:
            line = line.strip('\n,')
            if filename == "spr-ru.txt":
                doc = ast.literal_eval(line)
            else:
                doc = json.loads(line)
            for text_field in TEXT_COLUMNS[filename]:
                document_text = doc[text_field]
                if document_text is not None:
                    preprocessed_text = clean_text(document_text)
                    preprocessed_text = preprocessed_text.strip()
                    old_doc_id, new_doc_id = get_rudrec_doc_id(doc, filename, doc_id=i)
                    sentenized_text = sent_tokenize(preprocessed_text, language='russian')

                    if len(sentenized_text) > 0:
                        for sentence_id, sentence in enumerate(sentenized_text):
                            global_id += 1
                            sentence = sentence.replace('\n', ' ')
                            if new_doc_id is not None:
                                if old_doc_id != new_doc_id:
                                    map_file.write(f"{old_doc_id}\t{new_doc_id}\n")
                                json_entry = {
                                    "global_id" : global_id,
                                    "doc_id": new_doc_id,
                                    "sentence_id": sentence_id,
                                    "text": sentence,
                                }
                                json.dump(json_entry, output_file, ensure_ascii=False)
                                output_file.write("\n")
        except JSONDecodeError as e:
            print(e)
            print(line)
            print(filename)
        except TypeError as e:
            print("Type error")
            print(e)
            print(line)
    return global_id

def main():
    parser = ArgumentParser()
    parser.add_argument('--rudrec_dir', default=r'../RuDReC')
    parser.add_argument('--output_path', default=r'data_test.json')
    parser.add_argument('--id_map_path', default='url_mapping/rudrec_id_mapping_url.txt')
    args = parser.parse_args()

    corpus_directory = args.rudrec_dir
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    map_path = args.id_map_path
    output_dir = os.path.dirname(map_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    global_id = 1
    with codecs.open(output_path, "w+", encoding="utf-8") as output_file, \
            codecs.open(map_path, "w+", encoding="utf-8") as map_file:
        for filename in os.listdir(corpus_directory):
            print(filename)
            # assert filename in TEXT_COLUMNS.keys()
            if filename not in TEXT_COLUMNS.keys():
                continue
            file_path = os.path.join(corpus_directory, filename)
            with codecs.open(file_path, "r", encoding="utf-8") as inp:
                if PROCESS_AS_JSON_DOC[filename]:
                    global_id = fulldoc_to_json(input_file=inp, filename=filename, output_file=output_file,
                                                map_file=map_file, global_id=global_id)
                else:
                    global_id = jsondoc_linewise_to_json(input_file=inp, filename=filename, output_file=output_file,
                                                         map_file=map_file, global_id=global_id)


if __name__ == '__main__':
    main()
