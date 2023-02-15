import os
from pathlib import Path
import spacy
from spacy.symbols import ORTH
import re
from collections import defaultdict
import math

if __name__ == '__main__':
    # load model
    nlp = spacy.load("en_core_web_sm")
    # nlp = spacy.load("en_core_web_trf")

    # modify model
    infixes = nlp.Defaults.infixes + [r'(<)']
    nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer
    nlp.tokenizer.add_special_case(f"<i>", [{ORTH: f"<i>"}])
    nlp.tokenizer.add_special_case(f"</i>", [{ORTH: f"</i>"}])

    pages_dir = "../task1/pages/"
    pattern = '*.txt'
    pages = Path(pages_dir).glob(pattern)
    files_path = 'data/'
    if not os.path.exists(files_path):
        os.makedirs(files_path)
    tokens = defaultdict(lambda: defaultdict(int))
    lemmas = defaultdict(lambda: defaultdict(int))
    tokens2 = defaultdict(set)
    lemmas2 = defaultdict(set)
    for filename in pages:
        print(str(filename))
        with open(filename) as page:
            for line in page.readlines():
                doc = nlp(line)
                for word in doc:
                    # check if token consists of letters only and has type == ADJ or ADV or NOUN or PRON or VERB
                    if re.match(r"^[a-zA-Z]+$", word.text) and \
                            word.pos_ in {"ADJ", "ADV", "NOUN", "PRON", "VERB"} and \
                            word.text not in tokens:  # check if token haven't been added already
                        tokens[filename][word.text] += 1
                        lemmas[filename][word.lemma_] += 1
                        tokens2[filename].add(word.text)
                        lemmas2[filename].add(word.lemma_)
    pages_num = len(list(Path(pages_dir).glob(pattern)))
    print(pages_num)
    it = 0
    for filename in Path(pages_dir).glob(pattern):
        it += 1
        print(str(it) + ": " + str(filename))
        out1 = open(files_path + "tokens" + str(it) + ".txt", "w")
        out2 = open(files_path + "lemmas" + str(it) + ".txt", "w")
        for token in tokens2[filename]:
            out1.write(token + " ")
            count = 0
            for filename2 in Path(pages_dir).glob(pattern):
                if token in tokens2[filename2]:
                    count += 1
            idf = math.log(pages_num / count)
            out1.write(str(idf) + " ")
            tf = tokens[filename][token] / len(tokens[filename])
            tf_idf = tf * idf
            out1.write(str(tf_idf) + "\n")
        for lemma in lemmas2[filename]:
            out2.write(lemma + " ")
            count = 0
            for filename2 in Path(pages_dir).glob(pattern):
                if lemma in lemmas2[filename2]:
                    count += 1
            idf = math.log(float(pages_num) / count)
            out2.write(str(idf) + " ")
            tf = tokens[filename][lemma] / len(tokens[filename])
            tf_idf = tf * idf
            out2.write(str(tf_idf) + "\n")
        out1.close()
        out2.close()

