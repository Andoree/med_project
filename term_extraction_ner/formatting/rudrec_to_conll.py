import ast
import codecs
import json
import os
import re
from json import JSONDecodeError

from nltk import sent_tokenize, word_tokenize

TEXT_COLUMNS = {
    "all_reviews_texts.txt": ["description"],
    "comments.json": ["content", "pos_content", "neg_content"],
    "consumers_drugs_reviews.json": ["comment"],
    "doctors_drugs_reviews.json": ["comment", "comment_plus", "comment_minus"],
    "spr-ru.txt": ["text"]

}
PROCESS_AS_JSON_DOC = {
    "all_reviews_texts.txt": False,
    "comments.json": True,
    "consumers_drugs_reviews.json": True,
    "doctors_drugs_reviews.json": True,
    "spr-ru.txt": False
}


def list_replace(search, replacement, text):
    """
    Заменяет множество символов строки заданным
        :param search: строка заменяемых символов
        :param replacement: строка, которой заменяются заданные
        :param text: строка, в которой происходит поиск и замена
        :return: результат замены (строка)
    """
    search = [el for el in search if el in text]
    for c in search:
        text = text.replace(c, replacement)
    return text


def clean_text(text):
    # Унифицирование кавычек
    text = list_replace \
        ('\u00AB\u00BB\u2039\u203A\u201E\u201A\u201C\u201F\u2018\u201B\u201D\u2019', '\u0022', text)
    # Унифицирование тире
    text = list_replace \
        ('\u2012\u2013\u2014\u2015\u203E\u0305\u00AF', '\u2003\u002D\u002D\u2003', text)
    # Унифицирование дефисов и "минусов"
    text = list_replace('\u2010\u2011', '\u002D', text)
    # Унифицирование пробелов
    text = list_replace \
            (
            '\u2000\u2001\u2002\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B\u202F\u205F\u2060\u3000',
            '\u2002', text)

    text = re.sub('\u2003\u2003', '\u2003', text)
    text = re.sub('\t\t', '\t', text)

    # Унифицирование точек
    text = list_replace \
            (
            '\u02CC\u0307\u0323\u2022\u2023\u2043\u204C\u204D\u2219\u25E6\u00B7\u00D7\u22C5\u2219\u2062',
            '.', text)

    # Унифицирование "звёздочек"
    text = list_replace('\u2217', '\u002A', text)

    text = list_replace('…', '...', text)

    # Удаление диерезисов над латинскими буквами
    text = list_replace('\u00C4', 'A', text)
    text = list_replace('\u00E4', 'a', text)
    text = list_replace('\u00CB', 'E', text)
    text = list_replace('\u00EB', 'e', text)
    text = list_replace('\u1E26', 'H', text)
    text = list_replace('\u1E27', 'h', text)
    text = list_replace('\u00CF', 'I', text)
    text = list_replace('\u00EF', 'i', text)
    text = list_replace('\u00D6', 'O', text)
    text = list_replace('\u00F6', 'o', text)
    text = list_replace('\u00DC', 'U', text)
    text = list_replace('\u00FC', 'u', text)
    text = list_replace('\u0178', 'Y', text)
    text = list_replace('\u00FF', 'y', text)
    text = list_replace('\u00DF', 's', text)
    text = list_replace('\u1E9E', 'S', text)
    # text = list_replace(',.[]{}()=+-−*&^%$#@!~;:§/\|\"', ' ', text)
    # text = list_replace('0123456789', 'x', text)
    # text = list_replace(",.[]{}()=+-−*&^%$#@!~;:0123456789§/\|\"", " ", text)

    currencies = list \
            (
            '\u20BD\u0024\u00A3\u20A4\u20AC\u20AA\u2133\u20BE\u00A2\u058F\u0BF9\u20BC\u20A1\u20A0\u20B4\u20A7\u20B0\u20BF\u20A3\u060B\u0E3F\u20A9\u20B4\u20B2\u0192\u20AB\u00A5\u20AD\u20A1\u20BA\u20A6\u20B1\uFDFC\u17DB\u20B9\u20A8\u20B5\u09F3\u20B8\u20AE\u0192'
        )

    alphabet = list \
            (
            '\t\r абвгдеёзжийклмнопрстуфхцчшщьыъэюяАБВГДЕЁЗЖИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')

    # alphabet.append("'")

    # allowed = set(currencies + alphabet)
    #
    # cleaned_text = [sym for sym in text if sym in allowed]
    # cleaned_text = ''.join(cleaned_text)

    return text


def process_fulldoc_as_json(input_file, filename, output_file):
    file_text = input_file.read()
    docs = json.loads(file_text)
    i = 0
    for doc in docs:
        i += 1
        if i % 1000 == 0:
            print(filename, i)
        for text_field in TEXT_COLUMNS[filename]:
            document_text = doc[text_field]
            if document_text is not None:
                preprocessed_text = clean_text(document_text)
                preprocessed_text = preprocessed_text.strip()
                sentenized_text = sent_tokenize(preprocessed_text, language='russian')
                print(sentenized_text)
                if len(sentenized_text) > 0:
                    for sentence in sentenized_text:
                        words = word_tokenize(sentence, language='russian')
                        for word in words:
                            output_file.write(f"{word}\tO\n")
                        output_file.write('\n')


def process_jsondoc_linewise(input_file, filename, output_file):
    for line in input_file:
        try:
            line = line.strip('\n,')
            if filename == "spr-ru.txt":
                doc = ast.literal_eval(line)
            else:
                doc = json.loads(line)
            for text_field in TEXT_COLUMNS[filename]:
                document_text = doc[text_field]
                if document_text is not None:
                    preprocessed_text = clean_text(document_text)
                    preprocessed_text = preprocessed_text.strip()
                    sentenized_text = sent_tokenize(preprocessed_text, language='russian')
                    if len(sentenized_text) > 0:
                        for sentence in sentenized_text:
                            words = word_tokenize(sentence, language='russian')
                            for word in words:
                                output_file.write(f"{word}\tO\n")
                            output_file.write('\n')
        except JSONDecodeError as e:
            print(e)
            print(line)
            print(filename)
        except TypeError as e:
            print("Type error")
            print(e)
            print(line)


def main():
    corpus_directory = r"RuDReC/"
    output_path = 'data_test.txt'
    with codecs.open(output_path, "w+", encoding="utf-8") as output_file:
        for filename in os.listdir(corpus_directory):
            print(filename)
            # assert filename in TEXT_COLUMNS.keys()
            if not filename in TEXT_COLUMNS.keys():
                continue
            # assert filename in TEXT_COLUMNS.keys()
            file_path = os.path.join(corpus_directory, filename)
            with codecs.open(file_path, "r", encoding="utf-8") as inp:
                if PROCESS_AS_JSON_DOC[filename]:
                    process_fulldoc_as_json(input_file=inp, filename=filename, output_file=output_file)
                else:
                    process_jsondoc_linewise(input_file=inp, filename=filename, output_file=output_file)


if __name__ == '__main__':
    main()
