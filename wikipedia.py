"""The Wikipedia module downloads and parses articles through the Wiki API
   and cheches them for future use.
"""

import json
import logging
import re
import urllib.request
import urllib.parse
import requests


LOG = logging.getLogger('wikipedia')

SESSION = requests.session()


class Article:
    """Simple wrapper for downloading and parsing Wikipedia articles.
    """

    _EXTRACT_REGEX = re.compile(r'\[\[(.*?)(?:\||#|(?:\]\]))', re.I | re.M)

    def __init__(self, title):
        LOG.debug('Downloading "{}"...'.format(title))
        text = self._get_text(title)
        if text:
            self.links = self._get_links(text)
        else:
            self.links = []

    @staticmethod
    def _get_url(title):
        """Generate the URL to connect to the Wiki API.
        """

        encoded_title = urllib.parse.quote_plus(title)
        return ('https://en.wikipedia.org/w/api.php?format=json&action=query&prop='
                'revisions&rvprop=content&titles={}').format(encoded_title)

    @staticmethod
    def _title_normalize(title):
        """Normalize the article title according to the Wiki API standards.
        """

        title = title[0].upper() + title[1:]
        return "_".join(title.split())

    @classmethod
    def _get_links(cls, text):
        """Returns a list of all the links contained in an article.
        """

        matches = cls._EXTRACT_REGEX.findall(text)
        return list(set(cls._title_normalize(article) for article in matches
                        if article and ':' not in article))

    @classmethod
    def _get_data(cls, title):
        return SESSION.get(cls._get_url(title)).json()

    @classmethod
    def _get_text(cls, title):
        """Returns the entire article text.
        """

        data = cls._get_data(title)
        if not data:
            LOG.error('Failed to fetch data for "{}"'.format(title))
            return None

        page = next(iter(data['query']['pages'].values()))
        revisions = page.get('revisions', None)
        if not revisions:
            LOG.error('No revisions found for "{}"'.format(title))
            return None

        return revisions[0]['*']


class Wikipedia:
    """Manager for Wikipedia articles that caches results.
    """

    def __init__(self):
        self._articles = {}

    def get_article(self, article_title):
        if article_title in self._articles:
            return self._articles[article_title]
        return self._articles.setdefault(article_title, Article(article_title))
