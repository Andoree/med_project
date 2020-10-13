import os
from argparse import ArgumentParser
import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--wordnet_path',
                        default=r'../wordnet_meddra/all_wordnet_med_senses_synsets.tsv')
    parser.add_argument('--meddra_path',
                        default=r'../vocabs/vocabs_w_metadata/lemmatized_ru_meddra_vocab.tsv')
    parser.add_argument('--output_path', default=r'../wordnet_meddra/all_terms_wordnet_lemm_meddra_intersection.tsv')
    args = parser.parse_args()

    wordnet_path = args.wordnet_path
    meddra_path = args.meddra_path
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and output_dir != '':
        os.makedirs(output_dir)

    wordnet_df = pd.read_csv(wordnet_path, sep='\t', encoding="utf-8")
    meddra_df = pd.read_csv(meddra_path, sep='\t', encoding="utf-8")
    print(f"Wordnet size: {wordnet_df.shape[0]}")
    print(f"Meddra size: {meddra_df.shape[0]}")
    wordnet_df["sense_term"] = wordnet_df["sense_term"].apply(lambda x: x.lower())
    wordnet_df["synset_id_no_pos"] = wordnet_df["synset_id"].apply(lambda x: x[:-2])
    meddra_df["lemm_term"] = meddra_df["lemm_term"].apply(lambda x: x.lower())
    meddra_df["term"] = meddra_df["term"].apply(lambda x: x.lower())

    wn_meddra_joined_by_lemma_df = pd.merge(wordnet_df, meddra_df, left_on="sense_term", right_on="lemm_term",
                                            how="inner", )
    wn_meddra_joined_by_term_df = pd.merge(wordnet_df, meddra_df, left_on="sense_term", right_on="term", how="inner", )
    print(f"Term joined: {wn_meddra_joined_by_term_df.shape[0]}")
    print(f"Lemm joined: {wn_meddra_joined_by_lemma_df.shape[0]}")
    joined_df = pd.concat([wn_meddra_joined_by_lemma_df, wn_meddra_joined_by_term_df]).drop_duplicates()

    senses_whose_synsets_intersect_meddra_set = set(joined_df.synset_id_no_pos.values)
    all_senses_whose_synsets_intersect_meddra_df = wordnet_df[
        wordnet_df.synset_id_no_pos.isin(senses_whose_synsets_intersect_meddra_set)]

    print(f"Intersection size: {all_senses_whose_synsets_intersect_meddra_df.shape[0]}")
    print(f"Intersection unique senses: {len(set(all_senses_whose_synsets_intersect_meddra_df.sense_id.values))}")
    print(f"Intersection unique synsets: {len(set(all_senses_whose_synsets_intersect_meddra_df.synset_id.values))}")
    print(f"Intersection unique synsets no pos: {len(set(all_senses_whose_synsets_intersect_meddra_df.synset_id_no_pos.values))}")
    all_senses_whose_synsets_intersect_meddra_df.drop(columns=["synset_id_no_pos"], axis=1, inplace=True)
    all_senses_whose_synsets_intersect_meddra_df.to_csv(output_path, sep='\t', encoding="utf-8", index=False)



if __name__ == '__main__':
    main()
