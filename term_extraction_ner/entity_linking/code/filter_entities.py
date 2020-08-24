import os
from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_statistics', default=r'../../entities_statistics/statistics/entities_statistics.tsv')
    parser.add_argument('--output_path', default='../filtered_entities/entities_freq_ge_50.tsv')
    parser.add_argument('--min_freq', default=50, type=int)
    args = parser.parse_args()
    statistics_path = args.input_statistics
    output_path = args.output_path
    frequency_threshold = args.min_freq
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    stats_df = pd.read_csv(statistics_path, sep='\t')
    old_num_entities = stats_df.shape[0]
    stats_df = stats_df[stats_df.frequency >= frequency_threshold]
    stats_df.to_csv(output_path, '\t', index=False)
    print(f'Entities filtering is finished:\n'
          f'{old_num_entities} -> {stats_df.shape[0]} entities')


if __name__ == '__main__':
    main()
