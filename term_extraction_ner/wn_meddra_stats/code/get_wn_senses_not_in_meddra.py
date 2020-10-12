import os
from argparse import ArgumentParser
import pandas as pd
from xml.etree import ElementTree


def main():
    parser = ArgumentParser()
    parser.add_argument('--wn_senses', default=r'../wordnet_meddra/all_terms_wordnet_lemm_meddra_intersection.tsv')
    parser.add_argument('--wn_synsets_dir',
                        default=r'../wordnet/')
    parser.add_argument('--meddra_path',
                        default=r'../vocabs/vocabs_w_metadata/lemmatized_ru_meddra_vocab.tsv')
    parser.add_argument('--output_path', default=r'../wordnet_meddra/wn_senses_not_in_meddra_DELETE.tsv')
    args = parser.parse_args()

    senses_path = args.wn_senses
    synsets_dir = args.wn_synsets_dir
    meddra_path = args.meddra_path
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    wn_senses_df = pd.read_csv(senses_path, sep='\t', encoding="utf-8")
    print(wn_senses_df)
    meddra_df = pd.read_csv(meddra_path, sep='\t', encoding="utf-8")
    wn_senses_df["sense_term"] = wn_senses_df["sense_term"].apply(lambda x: x.lower())
    meddra_df["lemm_term"] = meddra_df["lemm_term"].apply(lambda x: x.lower())

    wn_synsets_from_meddra_set = set(wn_senses_df.synset_id.values)
    meddra_terms_set = set(meddra_df.lemm_term.values)
    # wn_senses_from_meddra_set = set(wn_senses_df.sense_id.values)

    term_types = ['N',  ]
    wn_senses_not_in_meddra = []
    for t_type in term_types:
        synsets_path = os.path.join(synsets_dir, f"synsets.{t_type}.xml")
        tree = ElementTree.parse(synsets_path)
        root = tree.getroot()

        for synset in root.findall("synset"):
            synset_id = synset.get('id')
            if synset_id in wn_synsets_from_meddra_set:
                for sense in synset.findall("sense"):
                    sense_id = sense.get('id')
                    sense_term = sense.text.lower()
                    if sense_term not in meddra_terms_set:
                        sense_dictionary = {
                            'synset_id': synset_id,
                            'sense_id': sense_id,
                            'sense_term': sense_term,
                        }
                        wn_senses_not_in_meddra.append(sense_dictionary)

    wn_senses_not_in_meddra_df = pd.DataFrame.from_records(wn_senses_not_in_meddra)
    print(wn_senses_not_in_meddra_df)
    print(f"Number of terms in meddra: {wn_senses_df.shape[0]}")
    print(f"Number of terms not in meddra: {wn_senses_not_in_meddra_df.shape[0]}")
    print(f"Wn senses in meddra: {len(wn_senses_df.sense_id.unique())}")
    print(f"Wn synsets in meddra: {len(wn_senses_df.synset_id.unique())}")
    print(f"Wn senses not in meddra: {len(wn_senses_not_in_meddra_df.sense_id.unique())}")
    print(f"Wn synsets not in meddra: {len(wn_senses_not_in_meddra_df.synset_id.unique())}")
    wn_senses_not_in_meddra_df.to_csv(output_path, sep='\t', index=False)


if __name__ == '__main__':
    main()
