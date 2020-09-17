import os
from argparse import ArgumentParser

from NLPDatasetIO.dataset import Dataset


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_path', default=r'data_test.json')
    parser.add_argument('--output_path', default=r'../data/otzovik_conll/test.tsv')
    parser.add_argument('--input_format', default='json')
    args = parser.parse_args()

    input_path = args.input_path
    input_format = args.input_format
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    dataset = Dataset(input_path, input_format)
    dataset.save('conll', path_to_save=output_path, sep='\t')


if __name__ == '__main__':
    main()
