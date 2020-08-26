import codecs
import json
import os
from argparse import ArgumentParser
import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument('--json_mapping', required=True)
    parser.add_argument('--output_path', required=True)
    args = parser.parse_args()

    input_json_path = args.json_mapping
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)
    with codecs.open(input_json_path, 'r', encoding='utf-8') as inp_file:
        entities_dicts_list = []
        for line in inp_file:
            json_doc = json.loads(line)
            entity_token = json_doc['text']
            mapping_candidates = json_doc['candidates']
            cand_tokens = []
            cand_concept_ids = []
            cand_distances = []
            for candidate_dict in mapping_candidates:
                candidate_token = candidate_dict['mapped_to']
                candidate_concept_id = candidate_dict['concept_id']
                candidate_distance = candidate_dict['distance']
                cand_tokens.append(candidate_token)
                cand_concept_ids.append(candidate_concept_id)
                cand_distances.append(candidate_distance)
            entity_cand_tokens_str = ','.join(cand_tokens)
            entity_cand_concpt_ids = ','.join(cand_concept_ids)
            entity_cand_distances = ','.join(cand_distances)
            entity_dict = {'entity': entity_token,
                           'mapping_tokens': entity_cand_tokens_str,
                           'mapping_concpt_ids': entity_cand_concpt_ids,
                           'mapping_distances': entity_cand_distances}
            entities_dicts_list.append(entity_dict)
        mapping_df = pd.DataFrame(entities_dicts_list)
        mapping_df.to_csv(output_path, sep='\t', index=False)


if __name__ == '__main__':
    main()
