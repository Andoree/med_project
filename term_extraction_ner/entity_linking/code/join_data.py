import codecs
import os
from argparse import ArgumentParser

import pandas as pd


YES_NO_DICT = {
    'yes' : 'no',
    'no' : 'yes'
}

def main():
    parser = ArgumentParser()
    parser.add_argument('--input_tsv_1', )
    parser.add_argument('--input_tsv_2', )
    parser.add_argument('--output_path', )
    parser.add_argument('--join_column', nargs='+', required=True)
    args = parser.parse_args()

    input_tsv_1 = args.input_tsv_1
    input_tsv_2 = args.input_tsv_2
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    join_column_1 = args.join_column[0]
    join_column_2 = args.join_column[1]

    data_df_1 = pd.read_csv(input_tsv_1, sep='\t', )
    data_df_2 = pd.read_csv(input_tsv_2, sep='\t', )
    data_df_2.rename(columns={join_column_2: join_column_1}, inplace=True)
    data_df_1[join_column_1] = data_df_1[join_column_1].apply(lambda x: '~'.join(x.split()))
    data_df_1[join_column_1] = data_df_1[join_column_1].astype(str)
    data_df_2[join_column_1] = data_df_2[join_column_1].astype(str)
   
    merged_df = data_df_1.merge(data_df_2, on=[join_column_1])
    merged_df.rename(columns={'Disease-related' : 'disease_related'}, inplace=True)
    merged_df['disease_related'] = merged_df['disease_related'].apply(lambda x: YES_NO_DICT[x])
    merged_df.to_csv(output_path, sep='\t', index=False)


if __name__ == '__main__':
    main()
