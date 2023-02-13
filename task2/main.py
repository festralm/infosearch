import re
import spacy
from spacy.symbols import ORTH
from pathlib import Path
from collections import defaultdict

if __name__ == '__main__':
    # load model
    nlp = spacy.load("en_core_web_sm")
    # nlp = spacy.load("en_core_web_trf")

    # modify model
    infixes = nlp.Defaults.infixes + [r'(<)']
    nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer
    nlp.tokenizer.add_special_case(f"<i>", [{ORTH: f"<i>"}])
    nlp.tokenizer.add_special_case(f"</i>", [{ORTH: f"</i>"}])

    directory = "../task1/pages/"
    files = Path(directory).glob('*.txt')
    out1 = open("tokens.txt", "w")
    out2 = open("lemmas.txt", "w")
    tokens = set()
    lemmas = defaultdict(list)
    it = 0
    for filename in files:
        it += 1
        print(str(it) + ": " + str(filename))
        with open(filename) as file:
            for line in file.readlines():
                doc = nlp(line)
                for token in doc:
                    # check if token consists of letters only and has type == ADJ or ADV or NOUN or PRON or VERB
                    if re.match(r"^[a-zA-Z]+$", token.text) and token.pos_ in {"ADJ", "ADV", "NOUN", "PRON", "VERB"} \
                            and token.text not in tokens:  # check if token haven't been added already
                        tokens.add(token.text)
                        out1.write(token.text + "\n")
                        lemmas[token.lemma_].append(token.text)

    out1.close()
    for k, v in lemmas.items():
        out2.write(k)
        for t in v:
            out2.write(" " + t)
        out2.write("\n")
    out2.close()