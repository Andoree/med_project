import os
from xml.etree import ElementTree
from argparse import ArgumentParser

import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--synset_relations',
                        default=r'../wordnet/synset_relations.N.xml')
    parser.add_argument('--synsets',
                        default=r'../wordnet/synsets.N.xml')
    parser.add_argument('--output_path', default=r'../wordnet/wordnet_med_senses_id_first.tsv')
    args = parser.parse_args()
    synset_relations = args.synset_relations
    synsets_path = args.synsets
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    tree = ElementTree.parse(synset_relations)
    root = tree.getroot()
    medical_synset_ids = set()
    for element in root.iter():
        tag = element.tag
        if tag == 'relation':
            rel_name = element.get('name')
            rel_child_id = element.get('child_id')
            rel_parent_id = element.get('parent_id')
            if rel_child_id == '1047-N':
                if rel_name == 'domain':
                    medical_synset_ids.add(rel_parent_id)
        else:
            pass

    tree = ElementTree.parse(synsets_path)
    root = tree.getroot()
    medical_senses = []
    for synset in root.findall("synset"):
        synset_id = synset.get('id')
        if synset_id in medical_synset_ids:
            for sense in synset.findall("sense"):
                sense_id = sense.get('id')
                sense_term = sense.text
                sense_dictionary = {
                    'sense_id': sense_id,
                    'sense_term': sense_term.lower(),

                }
                medical_senses.append(sense_dictionary)
    senses_df = pd.DataFrame.from_records(medical_senses)
    senses_df.to_csv(output_path, sep='\t', index=False)


if __name__ == '__main__':
    main()
