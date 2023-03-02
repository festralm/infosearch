import spacy
from spacy.symbols import ORTH
from pathlib import Path
import io
import re
from collections import defaultdict


class Tokenizer:
    def __init__(self):
        # load model
        self.nlp = spacy.load("ru_core_news_sm")

        # modify model
        infixes = self.nlp.Defaults.infixes + [r'(<)']
        self.nlp.tokenizer.infix_finditer = spacy.util.compile_infix_regex(infixes).finditer
        self.nlp.tokenizer.add_special_case(f"<i>", [{ORTH: f"<i>"}])
        self.nlp.tokenizer.add_special_case(f"</i>", [{ORTH: f"</i>"}])

        self.word_regex = r"^[а-яА-Я]+-?[а-яА-Я]+$"

    def get_tokens_and_lemmas(self, directory):
        """
        Retrieves tokens and lemmas from .txt files in the given directory
        :returns list of tokens and map lemma => tokens
        """
        files = Path(directory).glob('*.txt')
        it = 0
        tokens = set()
        lemmas = defaultdict(list)
        for filename in files:
            it += 1
            print(str(it) + ": " + str(filename))
            with io.open(filename, encoding='utf-8') as file:
                for line in file.readlines():
                    doc = self.nlp(line)
                    for token in doc:
                        # check if token consists of letters only and has type == ADJ or ADV or NOUN or PRON or VERB
                        if self.is_russian_token(token) \
                                and token.text not in tokens:  # check if token haven't been added already
                            tokens.add(token.text)
                            lemmas[token.lemma_].append(token.text)
        return tokens, lemmas

    def get_lemmas_to_files(self, directory):
        """
        Retrieves lemmas from .txt files in the given directory
        :returns map lemma => file names
        """
        files = Path(directory).glob('*.txt')
        lemma_to_files = {}
        it = 0
        for filename in files:
            file_name = str(filename)[len(directory):]
            it += 1
            lemmas = set()
            print(str(it) + ": " + file_name)
            with io.open(filename, encoding='utf-8') as file:
                for line in file.readlines():
                    doc = self.nlp(line)
                    for token in doc:
                        # check if lemma consists of letters only
                        # and has type == ADJ or ADV or NOUN or PRON or VERB
                        lemma = token.lemma_
                        if self.is_russian_token(token) \
                                and lemma not in lemmas:  # check if lemma hasn't been added already
                            lemmas.add(lemma)
                            if lemma in lemma_to_files.keys():
                                lemma_to_files[lemma].append(file_name)
                            else:
                                lemma_to_files[lemma] = [file_name]
        return lemma_to_files

    def is_russian_word(self, word):
        token = self.nlp(word)[0]
        return re.match(self.word_regex, token.text) \
            and token.pos_ in {"ADJ", "ADV", "NOUN", "PRON", "VERB"}

    def is_russian_token(self, token):
        return re.match(self.word_regex, token.text) \
            and token.pos_ in {"ADJ", "ADV", "NOUN", "PRON", "VERB"}

    def get_lemma_from_word(self, word):
        return self.nlp(word)[0].lemma_
