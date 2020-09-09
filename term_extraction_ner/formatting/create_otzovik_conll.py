from NLPDatasetIO.dataset import Dataset
from sklearn.model_selection import train_test_split


def main():
    dataset = Dataset('data/annotation', 'inception')

    train_documents, test_documents = train_test_split(dataset.documents, test_size=0.1, random_state=42)
    dataset.documents = train_documents
    dataset.save('conll', path_to_save='data/train.tsv', sep='\t')
    dataset.documents = test_documents
    dataset.save('conll', path_to_save='data/test.tsv', sep='\t')
    dataset.save('conll', path_to_save='data/dev.tsv', sep='\t')


if __name__ == '__main__':
    main()
