import codecs

from NLPDatasetIO.dataset import Dataset


def main():
    predicted_test_set = Dataset('../results_/predicted_biobert.txt', 'conll')
    output_path = r'predicted_biobert_sentences'
    with codecs.open(output_path, 'w+', encoding='utf-8') as output_file:
        for document in predicted_test_set.documents:
            output_file.write(f"{document.text.strip()}\n")


if __name__ == '__main__':
    main()
