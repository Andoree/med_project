import codecs

from NLPDatasetIO.dataset import Dataset


def main():
    predicted_test_set = Dataset('../results_/predicted_biobert.txt', 'conll')
    max_doc_id = -1
    for document in predicted_test_set.documents:
        max_doc_id = max(max_doc_id, document.doc_id)
    print(f"Max document id: {max_doc_id}")


if __name__ == '__main__':
    main()
