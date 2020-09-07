from collections import Counter
from typing import List, Dict


def single_word_to_symbolic_trigrams(word: str) -> List[str]:
    """
    :param word: An arbitrary string
    :return: List of symbolic trigrams which are present
    in the word string. The list might contain duplicated
    trigram strings.
    """
    trigrams_list = []
    if len(word) >= 3:
        for i in range(len(word) - 2):
            trigram = word[i:i + 3]
            trigrams_list.append(trigram)
    else:
        trigrams_list.append(word)
    return trigrams_list


def token_to_trigram_counter(token):
    """
    :param token: Ngram. Sequence of words divided by whitespaces.
    :return: Counter with token's trigram frequencies
    """
    token_counter_multiset = Counter()
    for word in token.split():
        word_trigrams_list = single_word_to_symbolic_trigrams(word)
        token_counter_multiset.update(word_trigrams_list)
    # todo: debug
    return token_counter_multiset


def calculate_symbolic_trigram_iou(token_1: str, token_2: str):
    """
    Calculates Intersection over Union (IoU) over substrings of
    length <=3 given the two ngrams
    :param token_1: Ngram. Sequence of words divided by whitespaces.
    :param token_2: Ngram. Sequence of words divided by whitespaces.
    :return:
    """
    token_1_counter_multiset = token_to_trigram_counter(token_1)
    token_2_counter_multiset = token_to_trigram_counter(token_2)

    intersection = token_1_counter_multiset & token_2_counter_multiset
    union = token_1_counter_multiset.copy()
    union.update(token_2_counter_multiset)
    iou_value = 2 * len(list(intersection.elements())) / len(list(union.elements()))
    return iou_value


def token_words_iou_metric(token_1: str, token_2: str):
    """
    Calculates intersection over union (IoU) for two strings.
    Data types of the elements of two lists should be the same.
    :return: iou value for the 2 given datasets
    """
    token_1 = set(token_1.split())
    token_2 = set(token_2.split())
    intersection = token_1.intersection(token_2)
    union = token_1.union(token_2)
    iou_value = len(intersection) / len(union)
    return iou_value


def calculate_row_columns_iou(row, iou_metric, entity_column: str,
                              vocab_column: str, vocab_to_lemm_dict: Dict[str,str]):
    """
    :param row: Pandas.Series
    :param iou_metric: Function that takes two tokens and returns a
    scalar value. Each token might consist of multiple words divided
    by whitespaces
    :param vocab_to_lemm_dict: Dict {concept : concept's lemma}
    :param vocab_column: Column name of a vocabulary's concept
    column
    :param entity_column: Column name of an entity's lemma column
    :return: IoU score for the values of two columns: vocab_column
    and entity_column.
    """

    entity_token = row[entity_column]
    vocab_token = row[vocab_column]
    lemm_vocab_token = vocab_to_lemm_dict[vocab_token]
    iou_score = iou_metric(entity_token, lemm_vocab_token)
    return iou_score


def list_replace(search, replacement, text):
    search = [el for el in search if el in text]
    for c in search:
        text = text.replace(c, replacement)
    return text
