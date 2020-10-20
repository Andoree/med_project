import os
from argparse import ArgumentParser
import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--meddra_path',
                        default=r'../vocabs/vocabs_w_metadata/lemmatized_ru_meddra_vocab.tsv')
    parser.add_argument('--wn_meddra_intersection',
                        default=r'../wordnet_meddra/all_terms_wordnet_lemm_meddra_intersection.tsv')
    parser.add_argument('--term_types', nargs='+', default=["PT", "LLT"])
    parser.add_argument('--output_df_path',
                        default=r'../wordnet_meddra/meddra_stats/wn_meddra_intersection_by_senses.tsv')
    parser.add_argument('--output_final_path',
                        default=r'../wordnet_meddra/meddra_stats/final_wn_meddra_intersection_by_senses.tsv')
    parser.add_argument('--output_stats_path', default=r'../wordnet_meddra/meddra_stats/pt_stats.txt')
    args = parser.parse_args()

    meddra_path = args.meddra_path
    wn_meddra_intersection_path = args.wn_meddra_intersection
    term_types_list = args.term_types
    output_senses_in_meddra_path = args.output_df_path
    output_dir = os.path.dirname(output_senses_in_meddra_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    output_stats_path = args.output_stats_path
    output_dir = os.path.dirname(output_stats_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    output_final_path = args.output_final_path
    output_dir = os.path.dirname(output_final_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    meddra_df = pd.read_csv(meddra_path, sep='\t', encoding="utf-8")
    intersection_senses_df = pd.read_csv(wn_meddra_intersection_path, sep='\t', encoding="utf-8")
    meddra_df["lemm_term"] = meddra_df["lemm_term"].apply(lambda x: x.lower())
    meddra_df["term"] = meddra_df["term"].apply(lambda x: x.lower())

    wn_meddra_joined_by_lemma_df = pd.merge(intersection_senses_df, meddra_df, left_on="sense_term",
                                            right_on="lemm_term",
                                            how="inner", )
    wn_meddra_joined_by_term_df = pd.merge(intersection_senses_df, meddra_df, left_on="sense_term", right_on="term",
                                           how="inner", )
    print(pd.concat([wn_meddra_joined_by_lemma_df, wn_meddra_joined_by_term_df]).shape)
    joined_df = pd.concat([wn_meddra_joined_by_lemma_df, wn_meddra_joined_by_term_df]).drop_duplicates()
    print(joined_df.shape)
    unique_meddra_codes = set(joined_df.ru_meddra_code.values)
    # Taking all CUIS that are present in wordnet-meddra intersection
    all_covered_cuis_set = set(joined_df.umls_cui.values)
    print(f"Unique meddra codes: {len(unique_meddra_codes)}")
    # Finding a set codes of PT instances of the wordnet-meddra intersection
    pt_df = joined_df[joined_df["term_type"].isin(term_types_list)]
    unique_pt_codes_from_intersection_set = set(pt_df.ru_meddra_code.values)
    unique_cuis_of_pt_codes_from_intersection_set = set(pt_df.umls_cui.values)
    print(f"Unique pt meddra codes: {len(unique_pt_codes_from_intersection_set)}")
    print(f"Unique meddra_codes: {len(unique_meddra_codes)}")
    print(f"Unique pt / Unique meddra codes: {len(unique_pt_codes_from_intersection_set) / len(unique_meddra_codes)}")
    full_meddra_pt_df = meddra_df[meddra_df["term_type"].isin(term_types_list)]
    full_meddra_pt_df = full_meddra_pt_df[full_meddra_pt_df.ru_meddra_code.isin(unique_meddra_codes)]
    unique_pt_codes_from_meddra_set = set(full_meddra_pt_df.ru_meddra_code.values)
    print(
        f"All meddra Unique pt / Unique meddra codes: {len(unique_pt_codes_from_meddra_set) / len(unique_meddra_codes)}")

    # Excluding CUIS that has a term with PT type from wordnet-lemma intersection
    all_covered_cuis_set = all_covered_cuis_set.difference(unique_cuis_of_pt_codes_from_intersection_set)
    # Getting meddra terms with CUIs that do not have a PT in wordnet-meddra intersection
    meddra_pt_codes_df = meddra_df[meddra_df.umls_cui.isin(all_covered_cuis_set)]
    # Filtering out all terms that are not of type PT
    meddra_pt_codes_df = meddra_pt_codes_df[meddra_pt_codes_df.term_type.isin(term_types_list)]
    # Getting a list of CUIs that have a PT but not in wordnet-meddra intersection
    meddra_cuis_with_pt_set = set(meddra_pt_codes_df.umls_cui.values)

    # Excluding PTs' CUIs that are not in wordnet-meddra intersection but have a
    # PT term in Meddra
    all_covered_cuis_set = all_covered_cuis_set.difference(meddra_cuis_with_pt_set)
    joined_df = joined_df[joined_df.umls_cui.isin(all_covered_cuis_set)]
    no_pt_codes_set = set(joined_df.ru_meddra_code.values)
    print(f"No PT codes / Unique meddra codes: {1 - len(no_pt_codes_set) / len(unique_meddra_codes)}")

    joined_df.to_csv(output_senses_in_meddra_path, sep='\t', encoding="utf-8", index=False)
    with open(output_stats_path, 'w+', encoding="utf-8") as output_file:
        output_file.write(f"Unique pt meddra codes: {len(unique_pt_codes_from_intersection_set)}\n")
        output_file.write(f"Unique meddra_codes: {len(unique_meddra_codes)}\n")
        output_file.write(
            f"Unique pt / Unique meddra codes: {len(unique_pt_codes_from_intersection_set) / len(unique_meddra_codes)}\n")
        output_file.write(
            f"All meddra Unique pt / Unique meddra codes: {len(unique_pt_codes_from_meddra_set) / len(unique_meddra_codes)}\n")
        output_file.write(f"No PT codes / Unique meddra codes: {len(no_pt_codes_set) / len(unique_meddra_codes)}\n")
        output_file.write(
            f"terms, that have a PT with the same CUI / Unique meddra codes: {1 - len(no_pt_codes_set) / len(unique_meddra_codes)}\n")


if __name__ == '__main__':
    main()
