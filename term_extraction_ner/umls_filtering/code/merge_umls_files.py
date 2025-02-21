import codecs
import os
from argparse import ArgumentParser
import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--groups_file', required=True)
    parser.add_argument('--vocab_path', required=True)
    parser.add_argument('--keep_columns_file', required=True)
    parser.add_argument('--output_path', required=True)
    args = parser.parse_args()

    groups_path = args.groups_file
    vocab_path = args.vocab_path
    column_name_mapping_path = args.keep_columns_file
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    column_rename_map = {}
    with codecs.open(column_name_mapping_path, 'r', encoding='utf-8') as inp_file:
        for line in inp_file:
            line = line.strip()
            attrs = line.split("|")
            rename_from = attrs[0]
            rename_to = attrs[1]
            column_rename_map[rename_from] = rename_to
    keep_columns_list = list(column_rename_map.keys())
    groups_df = pd.read_csv(groups_path, sep='|', header=None,
                            names=['Semantic Group Abbrev', 'Semantic Group Name', 'TUI', 'Full Semantic Type Name'])
    vocab_df = pd.read_csv(vocab_path, sep='\t', )
    merged_df = pd.DataFrame.merge(groups_df, vocab_df, on="TUI")
    filtered_merged_df = merged_df[keep_columns_list]
    filtered_merged_df.rename(
        columns=column_rename_map, inplace=True)
    print(filtered_merged_df.head())
    filtered_merged_df.to_csv(output_path, sep='\t', index=None)


if __name__ == '__main__':
    main()
