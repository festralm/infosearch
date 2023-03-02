import json
import codecs
from task2.tokenizer import Tokenizer
import re

NOT = 'not'
AND = 'and'
OR = 'or'


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def difference(list1, list2):
    diff = []
    for element in list1:
        if element not in list2:
            diff.append(element)
    return diff


def merge(list1, list2):
    return list(set(list1 + list2))


if __name__ == '__main__':
    tokenizer = Tokenizer()

    search_str = input()
    search_str = re.sub(r'\s+', ' ', search_str)

    split_or = search_str.split(f' {OR} ')

    query = []
    for or_item in split_or:
        ands = {}
        split_and = or_item.split(f' {AND} ')
        ands[AND] = []
        ands[NOT] = []
        for i in range(len(split_and)):
            and_item = split_and[i]
            word = ''
            if and_item.startswith(f'{NOT} '):
                word = and_item[4:]
                ands[NOT].append(tokenizer.get_lemma_from_word(word))
            else:
                word = and_item
                ands[AND].append(tokenizer.get_lemma_from_word(word))
            if not tokenizer.is_russian_word(word):
                raise Exception("Not a russian token")
        query.append(ands)

    inverted_index_file = codecs.open("inverted_index.json", "r", "utf-8")
    inverted_index_json = json.load(inverted_index_file)

    result = []
    base = []
    for key in inverted_index_json:
        base.extend(x for x in inverted_index_json[key] if x not in base)
    for or_item in query:
        current_result = base
        for k, v in or_item.items():
            for and_item in v:
                file_names = inverted_index_json[and_item] if and_item in inverted_index_json else []
                if k == AND:
                    current_result = intersection(current_result, file_names)
                elif k == NOT:
                    current_result = difference(current_result, file_names)
        result = merge(result, current_result)

    print(sorted(result))
