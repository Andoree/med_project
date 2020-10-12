import os
from xml.etree import ElementTree
from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--synset_relations', nargs='+',
                        default=[r'../wordnet/synset_relations.A.xml',
                                 r'../wordnet/synset_relations.N.xml',
                                 r'../wordnet/synset_relations.V.xml'])
    parser.add_argument('--synsets', nargs='+',
                        default=[r'../wordnet/synsets.A.xml',
                                 r'../wordnet/synsets.V.xml',
                                 r'../wordnet/synsets.N.xml'])
    parser.add_argument('--synset_id', nargs='+',
                        default=[r'1047-N', r'1047-A', r'1047-V', ])
    parser.add_argument('--output_path', default=r'../wordnet_meddra/all_wordnet_med_senses_synsets.tsv')
    args = parser.parse_args()

    synset_relations_list = args.synset_relations
    synsets_paths_list = args.synsets
    synset_ids_list = args.synset_id
    print('ddd', synset_ids_list)
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    medical_synset_ids_set = set()
    for synset_relations_path in synset_relations_list:
        tree = ElementTree.parse(synset_relations_path)
        root = tree.getroot()
        for element in root.iter():
            tag = element.tag
            if tag == 'relation':
                rel_name = element.get('name')
                rel_child_id = element.get('child_id')
                rel_parent_id = element.get('parent_id')
                if rel_child_id in synset_ids_list:
                    if rel_name == 'domain':
                        medical_synset_ids_set.add(rel_parent_id)
            else:
                pass
    print(f"Found medical synsets: {len(medical_synset_ids_set)}")
    medical_senses = []

    for synsets_path in synsets_paths_list:
        tree = ElementTree.parse(synsets_path)
        root = tree.getroot()
        for synset in root.findall("synset"):
            synset_ids_list = synset.get('id')
            if synset_ids_list in medical_synset_ids_set:
                for sense in synset.findall("sense"):
                    sense_id = sense.get('id')
                    sense_term = sense.text
                    sense_dictionary = {
                        'synset_id': synset_ids_list,
                        'sense_id': sense_id,
                        'sense_term': sense_term.lower(),
                    }
                    medical_senses.append(sense_dictionary)
    senses_df = pd.DataFrame.from_records(medical_senses)
    senses_df.to_csv(output_path, sep='\t', index=False)


if __name__ == '__main__':
    main()
