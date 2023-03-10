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

        self.word_regex = r"^[а-яА-Я]+(-?[а-яА-Я]+)?$"

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

    def get_tokens_and_lemmas_and_counts(self, directory):
        pattern = '*.txt'
        pages = Path(directory).glob(pattern)
        tokens = defaultdict(lambda: defaultdict(int))
        lemmas = defaultdict(lambda: defaultdict(int))
        tokens2 = defaultdict(set)
        lemmas2 = defaultdict(set)
        for filename in pages:
            filename_str = str(filename)[len(directory):]
            print(filename_str)
            with io.open(filename, encoding='utf-8') as page:
                for line in page.readlines():
                    doc = self.nlp(line)
                    for token in doc:
                        if self.is_russian_token(token):
                            tokens[filename_str][token.text] += 1
                            lemmas[filename_str][token.lemma_] += 1
                            tokens2[filename_str].add(token.text)
                            lemmas2[filename_str].add(token.lemma_)

        return tokens, lemmas, tokens2, lemmas2

    def get_lemmas_to_files(self, directory):
        """
        Retrieves lemmas from .txt files in the given directory
        :returns map lemma => file names
        """
        files = Path(directory).glob('*.txt')
        lemma_to_files = {}
        it = 0
        for filename in files:
            filename_str = str(filename)[len(directory):]
            it += 1
            lemmas = set()
            print(str(it) + ": " + filename_str)
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
                                lemma_to_files[lemma].append(filename_str)
                            else:
                                lemma_to_files[lemma] = [filename_str]
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
