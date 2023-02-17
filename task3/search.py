import json
import codecs

if __name__ == '__main__':
    search_str = input()

    # words = search_str.split(' ')
    inverted_index_file = codecs.open("inverted_index.json", "w", "utf-8")
    inverted_index_json = json.load(inverted_index_file)


    print(inverted_index_json)
