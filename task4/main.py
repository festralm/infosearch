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
        filename_str = str(filename)[len(pages_dir):]
        print(str(it) + ": " + filename_str)
        out1 = codecs.open(files_path + "tokens" + str(it) + ".txt", "w", "utf-8")
        out2 = codecs.open(files_path + "lemmas" + str(it) + ".txt", "w", "utf-8")
        for token in tokens2[filename_str]:
            out1.write(token + " ")
            count = 0
            for filename2 in Path(pages_dir).glob(pattern):
                filename2_str = str(filename2)[len(pages_dir):]
                if token in tokens2[filename2_str]:
                    count += 1
            idf = math.log(float(pages_num) / count)
            out1.write(str(idf) + " ")
            tf = tokens[filename_str][token] / len(tokens[filename_str])
            tf_idf = tf * idf
            out1.write(str(tf_idf) + "\n")
        out1.close()
        for lemma in lemmas2[filename_str]:
            out2.write(lemma + " ")
            count = 0
            for filename2 in Path(pages_dir).glob(pattern):
                filename2_str = str(filename2)[len(pages_dir):]
                if lemma in lemmas2[filename2_str]:
                    count += 1
            idf = math.log(float(pages_num) / count)
            out2.write(str(idf) + " ")
            tf = lemmas[filename_str][lemma] / len(lemmas[filename_str])
            tf_idf = tf * idf
            out2.write(str(tf_idf) + "\n")
        out2.close()

