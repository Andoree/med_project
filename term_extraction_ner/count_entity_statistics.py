import argparse
import codecs


class EntityLemm:

    def __init__(self, lemm_ngram, pos):
        self.lemm_ngram = lemm_ngram
        self.ngram_forms_freqs = {}
        self.entity_types = set()
        self.pos = pos

    def get_ngram_frequency(self):
        lemm_frequency = 0
        for ngram_frequency in self.ngram_forms_freqs.values():
            lemm_frequency += ngram_frequency
        return lemm_frequency

    def get_ordered_by_freq_forms(self):
        form_freq = [(form, freq) for form, freq in self.ngram_forms_freqs.items()]
        form_freq.sort(key=lambda t: -t[1])
        form_freq = [t[0] for t in form_freq]
        return form_freq

    def update_ngram_forms(self, ngram, entity_type):
        if self.ngram_forms_freqs.get(ngram) is None:
            self.ngram_forms_freqs[ngram] = 0
        self.ngram_forms_freqs[ngram] += 1
        self.entity_types.add(entity_type)

    def __hash__(self):
        return hash((self.lemm_ngram))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.lemm_ngram == other.lemm_ngram


def is_label_list_disease_related(entity_types_list):
    for ent_type in entity_types_list:
        if 'Drug' not in ent_type:
            return False
    return True


def write_entities_to_file(entities, filename, header_columns):
    with codecs.open(filename, 'w+', encoding='utf-8') as output_file:
        output_file.write('\t'.join(header_columns))
        output_file.write('\n')
        for entity_lemm in entities:
            entity_types = entity_lemm.entity_types
            is_entity_disease_related = is_label_list_disease_related(entity_types)
            is_entity_disease_related = 'yes' if is_entity_disease_related else 'no'
            output_file.write(f"{entity_lemm.lemm_ngram}\t{entity_lemm.get_ngram_frequency()}\t"
                              f"{','.join(entity_types)}\t{entity_lemm.pos}"
                              f"\t{','.join(list(entity_lemm.get_ordered_by_freq_forms())[:5])}\t"
                              f"{is_entity_disease_related}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True,)
    parser.add_argument('--output_path', type=str, required=True,)
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path

    header = ['lemma', 'frequency', 'labels', 'POS', 'frequent_forms', 'Disease-related']
    entities_lemms = {}
    with codecs.open(input_path, 'r', encoding='utf-8') as input_file:
        for i, line in enumerate(input_file):
            attrs = line.strip().split('\t')
            if len(attrs) == 3:
                lemmatized_token_pos = attrs[0]
                token = attrs[1]
                lemmatized_words_pos = lemmatized_token_pos.split()
                lemmatized_token = '~'.join([x.split('_')[0] for x in lemmatized_words_pos])
                pos = '~'.join([x.split('_')[1] for x in lemmatized_words_pos])
                entity_type = attrs[2]
                entity_lemm = entities_lemms.get(lemmatized_token)
                if entity_lemm is None:
                    entity_lemm = EntityLemm(lemmatized_token, pos)
                    entities_lemms[lemmatized_token] = entity_lemm
                entity_lemm.update_ngram_forms(ngram=token, entity_type=entity_type)
            else:
                pass

    sorted_entities_lemms = [(x, x.get_ngram_frequency()) for x in entities_lemms.values()]
    sorted_entities_lemms.sort(key=lambda x: -x[1])
    sorted_entities_lemms = [t[0] for t in sorted_entities_lemms]
    write_entities_to_file(entities=sorted_entities_lemms, filename=output_path, header_columns=header)

    entities_type_list = ['Finding', 'ADR', 'Drugname', 'DI', 'Drugform', 'Drugclass']
    for entity_type in entities_type_list:
        output_filename = f"{entity_type}_stats.tsv"
        filtered_entities = []
        for entity_lemm in sorted_entities_lemms:
            if entity_type in entity_lemm.entity_types:
                filtered_entities.append(entity_lemm)
        write_entities_to_file(filtered_entities, output_filename, header_columns=header)


if __name__ == '__main__':
    main()
