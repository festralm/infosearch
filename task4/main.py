import os
from pathlib import Path
import math
from task2.tokenizer import Tokenizer
import codecs

if __name__ == '__main__':
    tokenizer = Tokenizer()

    pages_dir = "../task1/pages/"
    tokens, lemmas, tokens2, lemmas2 = tokenizer.get_tokens_and_lemmas_and_counts(pages_dir)

    files_path = 'data/'
    if not os.path.exists(files_path):
        os.makedirs(files_path)

    pattern = '*.txt'
    pages_num = len(list(Path(pages_dir).glob(pattern)))
    print(pages_num)
    it = 0
    for filename in Path(pages_dir).glob(pattern):
        it += 1
        print(str(it) + ": " + str(filename))
        out1 = codecs.open(files_path + "tokens" + str(it) + ".txt", "w", "utf-8")
        out2 = codecs.open(files_path + "lemmas" + str(it) + ".txt", "w", "utf-8")
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

