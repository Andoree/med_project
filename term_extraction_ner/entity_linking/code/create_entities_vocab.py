import codecs
import os
from argparse import ArgumentParser

import pandas as pd



def main():
    parser = ArgumentParser()
    parser.add_argument('--input_statistics', default=r'../filtered_entities/entities_freq_ge_50.tsv')
    parser.add_argument('--output_path', default='../filtered_entities/entities_vocab.txt')
    args = parser.parse_args()

    input_stats_path = args.input_statistics
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    stats_df = pd.read_csv(input_stats_path, sep='\t')
    entity_lemmas = stats_df['lemma'].apply(lambda lemma: ' '.join(lemma.split('~')))
    with codecs.open(output_path, 'w+', encoding='utf-8') as output_file:
        for lemma in entity_lemmas.values:
            print(lemma)
            output_file.write(f"{lemma}\n")




if __name__ == '__main__':
    main()
