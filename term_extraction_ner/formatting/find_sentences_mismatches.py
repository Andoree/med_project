import codecs


def check_sentences_matching(biobert_sentence, rudrec_sentence):
    biobert_sentence = biobert_sentence.replace('[UNK]', '')
    if biobert_sentence != rudrec_sentence:
        print("MISMATCH:")
        print(f"Biobert: |{biobert_sentence}|")
        print(f"Rudrec: |{rudrec_sentence}|")
        print('--------------------')
        return True
    return False


def main():
    biobert_predicted_path = r"../entities_statistics/code/predicted_biobert_sentences.txt"
    rudrec_sentences_path = r"rudrec_sentences.txt"
    with codecs.open(biobert_predicted_path, 'r', encoding='utf-8') as biobert_file, \
            codecs.open(rudrec_sentences_path, 'r', encoding='utf-8') as rudrec_file:
        biobert_sentence = biobert_file.readline().strip()
        rudrec_sentence = rudrec_file.readline().strip()
        previous_rudrec = None
        previous_biobert = None
        i = 1
        while biobert_sentence is not None and rudrec_sentence is not None:
            if i < 1000:
                if check_sentences_matching(biobert_sentence=biobert_sentence, rudrec_sentence=rudrec_sentence):
                    print('Previous biobert', previous_biobert)
                    print('Previous rudrec', previous_rudrec)
                    biobert_sentence = biobert_file.readline().strip()
                    if not check_sentences_matching(biobert_sentence=biobert_sentence, rudrec_sentence=rudrec_sentence):
                        raise Exception("EXCEPTION")
            else:
                break
            i += 1
            previous_rudrec = rudrec_sentence
            previous_biobert = biobert_sentence
            rudrec_sentence = rudrec_file.readline().strip()
            biobert_sentence = biobert_file.readline().strip()


if __name__ == '__main__':
    main()
