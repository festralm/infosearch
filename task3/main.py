import json
import codecs
from task2.tokenizer import Tokenizer

if __name__ == '__main__':
    tokenizer = Tokenizer()
    lemmas_to_files = tokenizer.get_lemmas_to_files("../task1/pages/")

    json_string = json.dumps(lemmas_to_files, ensure_ascii=False)
    with codecs.open("inverted_index.json", "w", "utf-8") as outfile:
        outfile.write(json_string)
