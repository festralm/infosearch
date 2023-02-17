import json
import io
import codecs
import pathlib
from pathlib import Path
import spacy
from spacy.symbols import ORTH
from collections import defaultdict
import re


def get_inverted_index():
    lemma_to_files = {}

    nlp = spacy.load("ru_core_news_sm")

    infixes = nlp.Defaults.infixes + [r'(<)']
    nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer
    nlp.tokenizer.add_special_case(f"<i>", [{ORTH: f"<i>"}])
    nlp.tokenizer.add_special_case(f"</i>", [{ORTH: f"</i>"}])

    directory = "../task1/pages/"
    files = Path(directory).glob('*.txt')
    it = 0
    for filename in files:
        file_name = str(filename)
        it += 1
        lemmas = set()
        print(str(it) + ": " + file_name)
        with io.open(filename, encoding='utf-8') as file:
            for line in file.readlines():
                doc = nlp(line)
                for token in doc:
                    # check if lemma consists of letters only
                    # and has type == ADJ or ADV or NOUN or PRON or VERB
                    lemma = token.lemma_
                    if re.match(r"^[а-яА-Я]+$", token.text) \
                            and token.pos_ in {"ADJ", "ADV", "NOUN", "PRON", "VERB"} \
                            and lemma not in lemmas:  # check if lemma hasn't been added already
                        lemmas.add(lemma)
                        if lemma in lemma_to_files.keys():
                            lemma_to_files[lemma].append(file_name)
                        else:
                            lemma_to_files[lemma] = [file_name]
    return lemma_to_files


if __name__ == '__main__':
    result = get_inverted_index()

    json_string = json.dumps(result, ensure_ascii=False)
    with codecs.open("inverted_index.json", "w", "utf-8") as outfile:
        outfile.write(json_string)
