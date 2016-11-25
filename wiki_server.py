"""The Flask server responsible with the database connection and data transmission.
"""

import json
import collections
from flask import Flask, render_template
from flask_cors import CORS
import postgres


APP = Flask(__name__)

CONNECTION = postgres.Connection('postgres', 'wiki')

CORS(APP)


@APP.route('/', methods=['GET', 'OPTIONS'])
def index():
    """The main function that renders the index page.
    """

    return render_template('index.html')

@APP.route('/api/links/<article_title>', methods=['GET'])
def get_links(article_title):
    """The API link that returns a list of the giver article's links.
    """

    link_rows = CONNECTION.query(
        'SELECT to_article FROM link WHERE lower(from_article)=%s',
        ("_".join(article_title.split()).lower(), )
    )
    links = [" ".join(title['to_article'].split("_")) for title in link_rows]
    return json.dumps(links)

@APP.route('/api/path/<from_article>&<to_article>', methods=['GET'])
def get_path(from_article, to_article):
    """The API link that returns the smallest distance between two articles.
    """

    queue = collections.deque([[from_article]])

    while queue:
        current_path = collections.deque.popleft(queue)
        links = json.loads(get_links(current_path[-1]))

        for link in links:
            new_path = current_path + [link]
            if link.lower() == to_article.lower():
                return " -> ".join(new_path)
            collections.deque.append(queue, new_path)

    return ""

if __name__ == '__main__':
    APP.run()
