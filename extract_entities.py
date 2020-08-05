import codecs

from NLPDatasetIO.dataset import Dataset


def main():
    predicted_test_set = Dataset('../predicted_biobert.txt', 'conll')
    output_filename = 'entities.tsv'
    with codecs.open(output_filename, 'w+', encoding='utf-8') as output_file:
        for x in predicted_test_set.documents:
            for entity in x.entities:
                output_file.write(f"{entity.text}\t{entity.type}\n")


if __name__ == '__main__':
    main()
