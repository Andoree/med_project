import ast
import codecs
import json
import os
from argparse import ArgumentParser
from json import JSONDecodeError

from otzovik_to_conll import TEXT_COLUMNS, PROCESS_AS_JSON_DOC, process_fulldoc_as_json, process_jsondoc_linewise
from term_extraction_ner.formatting.rudrec_to_conll import clean_text


def get_rudrec_doc_id(doc, filename):
    if filename == "all_reviews_texts.txt":
        doc_url = doc["url"]
        doc_id = doc_url.split('/')[-1].split('.')[0].split('_')[-1]
        doc_id = f"otzovik_{doc_id}"
    elif filename == "comments.json":
        doc_id = doc["id"]
        doc_id = f"comments_{doc_id}"
    elif filename == "consumers_drugs_reviews.json":
        doc_url = doc["url"]
        doc_id = doc_url.split('/')[-1]
        doc_id = f"consumers_{doc_id}"
    elif filename == "doctors_drugs_reviews.json":
        doc_url = doc["url"]
        doc_id = doc_url.split('/')[-1]
        doc_id = f"doctors_{doc_id}"
    elif filename == "spr-ru.txt":
        doc_id = doc.get("review_id")
        # if doc_id is None:
        #     print('spr-ru')
        #     print(doc.keys())
        #     print(doc['text'])
    else:
        raise Exception("Invalid filename in get_rudrec_doc_id function")
    return doc_id


def fulldoc_to_json(input_file, filename, output_file):
    file_text = input_file.read()
    docs = json.loads(file_text)
    i = 0
    for doc in docs:
        i += 1
        if i % 1000 == 0:
            print(filename, i)
        for text_field in TEXT_COLUMNS[filename]:
            document_text = doc[text_field]
            if document_text is not None:
                preprocessed_text = clean_text(document_text)
                preprocessed_text = preprocessed_text.strip()

                json_entry = {
                    "doc_id": get_rudrec_doc_id(doc, filename),
                    "text": preprocessed_text,
                    "entities": []
                }
                json.dump(json_entry, output_file, ensure_ascii=False)
                output_file.write("\n")


def jsondoc_linewise_to_json(input_file, filename, output_file):
    # docs_dict = {}
    for line in input_file:
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
                    doc_id = get_rudrec_doc_id(doc, filename)
                    if doc_id is not None:
                        json_entry = {
                            "doc_id": get_rudrec_doc_id(doc, filename),
                            "text": preprocessed_text,
                            "entities": []
                        }
                        json.dump(json_entry, output_file, ensure_ascii=False)
                        output_file.write("\n")

                    # if docs_dict.get(preprocessed_text) is None:
                    #     docs_dict[preprocessed_text] = doc
                    # else:
                    #     doc_2 = docs_dict[preprocessed_text]
                    #     for key, value in doc.items():
                    #         doc_2[key] = value
                    #     docs_dict[preprocessed_text] = doc_2
        except JSONDecodeError as e:
            print(e)
            print(line)
            print(filename)
        except TypeError as e:
            print("Type error")
            print(e)
            print(line)
    # for preprocessed_text, doc in docs_dict.items():
    #     doc_id = get_rudrec_doc_id(doc, filename)
    #     if doc_id is not None:
    #         json_entry = {
    #             "doc_id": get_rudrec_doc_id(doc, filename),
    #             "text": preprocessed_text,
    #             "entities": []
    #         }
    #         json.dump(json_entry, output_file)


def main():
    parser = ArgumentParser()
    parser.add_argument('--rudrec_dir', default=r'RuDReC/')
    parser.add_argument('--output_path', default=r'data_test.json')
    args = parser.parse_args()

    corpus_directory = args.rudrec_dir
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    output_path = 'data_test.json'
    with codecs.open(output_path, "w+", encoding="utf-8") as output_file:
        for filename in os.listdir(corpus_directory):
            print(filename)
            # assert filename in TEXT_COLUMNS.keys()
            if filename not in TEXT_COLUMNS.keys():
                continue
            # assert filename in TEXT_COLUMNS.keys()
            file_path = os.path.join(corpus_directory, filename)
            with codecs.open(file_path, "r", encoding="utf-8") as inp:
                if PROCESS_AS_JSON_DOC[filename]:
                    fulldoc_to_json(input_file=inp, filename=filename, output_file=output_file)
                else:
                    jsondoc_linewise_to_json(input_file=inp, filename=filename, output_file=output_file)


if __name__ == '__main__':
    main()
