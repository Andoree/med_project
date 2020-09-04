import os
from argparse import ArgumentParser
import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--groups_file', required=True)
    parser.add_argument('--vocab_path', required=True)
    parser.add_argument('--output_path', required=True)
    args = parser.parse_args()

    groups_path = args.groups_file
    vocab_path = args.vocab_path
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    groups_df = pd.read_csv(groups_path, sep='|', header=None,
                            names=['Semantic Group Abbrev', 'Semantic Group Name', 'TUI', 'Full Semantic Type Name'])
    vocab_df = pd.read_csv(vocab_path, sep='\t', )
    merged_df = pd.DataFrame.merge(groups_df, vocab_df, on="TUI")
    filtered_merged_df = merged_df[
        ['CUI', 'TUI', 'Semantic Group Abbrev', 'SCUI', 'STR', 'Full Semantic Type Name',
         'Semantic Group Name']]
    filtered_merged_df.rename(
        columns={'Semantic Group Abbrev': 'semantic_group', 'CUI': 'umls_cui',
                 'Semantic Group': 'semantic_group_name', 'SCUI': 'meshrus_cui',
                 'Full Semantic Type Name': 'semantic_type_name',
                 'TUI': 'semantic_type', 'STR': 'term', 'Semantic Group Name' : 'semantic_group_name'}, inplace=True)
    print(filtered_merged_df.head())
    filtered_merged_df.to_csv(output_path, sep='\t', index=None)


if __name__ == '__main__':
    main()
