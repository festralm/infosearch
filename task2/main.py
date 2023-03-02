import codecs
from tokenizer import Tokenizer

if __name__ == '__main__':

    tokenizer = Tokenizer()

    tokens, lemmas = tokenizer.get_tokens_and_lemmas("../task1/pages/")

    out1 = codecs.open("tokens.txt", "w", "utf-8")
    for token in tokens:
        out1.write(token + "\n")
    out1.close()

    out2 = codecs.open("lemmas.txt", "w", "utf-8")
    for k, v in lemmas.items():
        out2.write(k)
        for t in v:
            out2.write(" " + t)
        out2.write("\n")
    out2.close()
