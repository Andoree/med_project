import os
from argparse import ArgumentParser
import pandas as pd
from xml.etree import ElementTree


def main():
    parser = ArgumentParser()
    parser.add_argument('--wn_meddra_intersection',
                        default=r'../wordnet_meddra/wn_pt_lltmeddra_intersection/pt_llt_wordnet_lemm_meddra_intersection.tsv')
    parser.add_argument('--wn_med_full',
                        default=r'../wordnet_meddra/all_wordnet_med_senses_synsets.tsv')
    parser.add_argument('--meddra_path',
                        default=r'../vocabs/vocabs_w_metadata/pt_llt_lemmatized_ru_meddra_vocab.tsv')
    parser.add_argument('--output_path',
                        default=r'../wordnet_meddra/wn_pt_lltmeddra_intersection/pt_llt_wn_senses_not_in_meddra.tsv')
    args = parser.parse_args()

    wn_meddra_intersection_path = args.wn_meddra_intersection
    wn_med_full_path = args.wn_med_full
    meddra_path = args.meddra_path
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    intersection_senses_df = pd.read_csv(wn_meddra_intersection_path, sep='\t', encoding="utf-8")
    intersection_senses_df["synset_id_no_pos"] = intersection_senses_df["synset_id"].apply(lambda x: x[:-2])
    wn_med_full_df = pd.read_csv(wn_med_full_path, sep='\t', encoding="utf-8")
    wn_med_full_df["synset_id_no_pos"] = wn_med_full_df["synset_id"].apply(lambda x: x[:-2])
    meddra_df = pd.read_csv(meddra_path, sep='\t', encoding="utf-8")
    intersection_senses_df["sense_term"] = intersection_senses_df["sense_term"].apply(lambda x: x.lower())
    meddra_df["lemm_term"] = meddra_df["lemm_term"].apply(lambda x: x.lower())
    meddra_df["term"] = meddra_df["term"].apply(lambda x: x.lower())

    wn_synsets_from_meddra_set = set(intersection_senses_df.synset_id_no_pos.values)
    meddra_lemm_terms_set = set(meddra_df.lemm_term.values)
    meddra_terms_set = set(meddra_df.term.values)
    meddra_terms_set = meddra_terms_set.union(meddra_lemm_terms_set)

    # all_wordnet_med_terms_set = set(wn_med_full_df.sense_term.values)
    wn_filtered_senses_df = wn_med_full_df[wn_med_full_df.synset_id_no_pos.isin(wn_synsets_from_meddra_set)]
    wn_filtered_senses_df = wn_filtered_senses_df[~wn_filtered_senses_df.sense_term.isin(meddra_terms_set)]
    wn_filtered_senses_df.drop(columns=["synset_id_no_pos"], axis=1, inplace=True)
    assert len(set(wn_filtered_senses_df.sense_term).intersection(meddra_terms_set)) == 0
    print("result")
    print(wn_filtered_senses_df)
    print(f"Wn senses in meddra: {len(intersection_senses_df.sense_id.unique())}")
    print(f"Wn synsets in meddra: {len(intersection_senses_df.synset_id.unique())}")
    print(f"Wn senses not in meddra: {len(wn_filtered_senses_df.sense_id.unique())}")
    print(f"Wn synsets not in meddra: {len(wn_filtered_senses_df.synset_id.unique())}")
    wn_filtered_senses_df.to_csv(output_path, sep='\t', index=False)


if __name__ == '__main__':
    main()
