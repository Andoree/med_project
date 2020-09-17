import os
from argparse import ArgumentParser

from NLPDatasetIO.dataset import Dataset


def main():
    parser = ArgumentParser()
    parser.add_argument('--rudrec_json', default=r'data_test.json')
    parser.add_argument('--output_path', default=r'../data/otzovik_conll/test.tsv')
    args = parser.parse_args()

    rudrec_json_path = args.rudrec_json
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    dataset = Dataset(rudrec_json_path, 'json')
    dataset.save('conll', path_to_save=output_path, sep='\t')


if __name__ == '__main__':
    main()
