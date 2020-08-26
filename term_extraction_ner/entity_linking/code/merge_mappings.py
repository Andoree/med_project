import codecs
import json
import os
from argparse import ArgumentParser

import pandas as pd

CORPUS_ID_MAPPING = {
    'meddra': 'CUI',
    'wordnet': 'sense_id',
    'mesh': 'CUI'
}


def main():
    parser = ArgumentParser()
    parser.add_argument('--input_tsvs', nargs='+', required=True)
    parser.add_argument('--output_path', required=True)
    parser.add_argument('--corpora_names', nargs='+', required=True)
    args = parser.parse_args()

    input_tsvs = args.input_tsv
    corpora_names = args.corpora_names
    output_path = args.output_path
    assert len(corpora_names) == len(input_tsvs)
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    dataframes_list = []
    for i in range(len(corpora_names)):
        corpus_name = corpora_names[i]
        input_tsv_path = input_tsvs[i]
        id_name = CORPUS_ID_MAPPING[corpus_name]
        mapping_df = pd.read_csv(input_tsv_path, sep='\t')
        mapping_df = mapping_df[['entity', 'mapping_tokens', 'mapping_concpt_ids', 'mapping_distances']]
        mapping_df.rename(columns={'entity': 'entity', 'mapping_tokens': f'{corpus_name}_term',
                                   'mapping_concpt_ids': f'{corpus_name}_{id_name}',
                                   'mapping_distances': f"{corpus_name}_distance"}, inplace=True)
        mapping_df.to_csv(output_path, sep='\t', index=False)
        print(corpus_name, mapping_df.shape)
        dataframes_list.append(mapping_df)

    result_df = pd.concat(dataframes_list, axis=1, join='inner')
    result_df.to_csv(output_path, sep='\t', index=False)


if __name__ == '__main__':
    main()
