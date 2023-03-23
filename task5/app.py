# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import json, sys
import requests
from pathlib import Path
import io
from task2.tokenizer import Tokenizer
import re

app = Flask(__name__)
bootstrap = Bootstrap(app)

link_to_lemma_to_tfidf = {}


@app.route('/')
def index():
    return render_template('index.html', name='index')


def get_pages(q, start_index, count):
    tokenizer = Tokenizer()

    if start_index + count > 100:
        if count > 100:
            count = 100
        start_index = 100 - count

    words = re.findall(r'\w+', q)

    words = [tokenizer.get_lemma_from_word(word) for word in words]

    link_to_sum = {}

    for link, lemma_to_tfidf in link_to_lemma_to_tfidf.items():
        link_to_sum[link] = 0
        for word in words:
            if word in lemma_to_tfidf.keys():
                link_to_sum[link] = link_to_sum[link] + lemma_to_tfidf[word]

    link_to_sum = sorted(link_to_sum.items(), key=lambda item: item[1], reverse=True)

    result = {}

    result['queries'] = {}
    result['queries']['request'] = []
    result['queries']['request'].appens({})
    result['queries']['request'][0]['startIndex'] = start_index + 1

    result['items'] = []

    for link in link_to_sum[start_index:start_index + count]:
        item = {}
        item['htmlTitle'] = link[0]
        item['link'] = link[0]
        item['htmlFormattedUrl'] = link[0]

    return result


@app.route('/query/', methods=['GET'])
def query():
    if request.method == 'GET':
        count = 10
        q = request.args.get('q')
        start_index = request.args.get('start')

        data = get_pages(q, start_index, count)
        results = []
        items = data['items']
        current_start_index = data['queries']['request'][0]['startIndex']
        page_index = (current_start_index - 1) / count + 1

        if current_start_index == 1:
            has_previous = 0
        else:
            has_previous = 1

        print(items)
        for item in items:
            result = {
                "title": item['htmlTitle'],
                "link": item['link'],
                "displayLink": item['htmlFormattedUrl']
            }
            results.append(result)
        return render_template('index.html', q=q, results=results, has_previous=has_previous,
                               current_start_index=current_start_index, page_index=page_index)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


def fill_link_map():
    index = {}
    with io.open("../task1/index.txt", encoding='utf-8') as file:
        for line in file.readlines():
            name_to_link = line.split(' ')
            index[name_to_link[0].replace(":", "")] = name_to_link[1].replace("\n", "")

    directory = "../task4/data/"
    files = Path(directory).glob('lemmas*')
    for filename in files:
        normalized_filename = "pages/" + str(filename)[len(directory) + 6:]
        link_to_lemma_to_tfidf[index[normalized_filename]] = {}
        lemma_to_tfidf = link_to_lemma_to_tfidf[index[normalized_filename]]
        with io.open(filename, encoding='utf-8') as file:
            for line in file.readlines():
                line_metrics = line.split(' ')
                lemma_to_tfidf[line_metrics[0]] = float(line_metrics[2])


if __name__ == '__main__':
    fill_link_map()
    app.run(debug=True)
