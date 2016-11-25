"""A web crawler that indexes wikipedia articles with their contained links in the 'wiki' database.
"""

import uuid
import logging
import sys
import postgres
import wikipedia


LOG = logging.getLogger('crawler')

CONNECTION = postgres.Connection('postgres', 'wiki')


def get_articles(crawler_id):
    """Provides articles to a crawler and updates the database.
    """

    rows = CONNECTION.query(
        'UPDATE article '
        'SET '
        '   assigned_crawler_id = %s,'
        '   assigned_crawler_time = NOW() '
        'WHERE name IN ('
        '   SELECT name'
        '   FROM article'
        '   WHERE'
        '       assigned_crawler_id IS NULL OR'
        '       NOW() - assigned_crawler_time > interval %s OR'
        '       NOW() - last_crawled > interval %s'
        '   FOR UPDATE SKIP LOCKED'
        '   LIMIT %s'
        ')'
        'RETURNING name;',
        (crawler_id, '60 minutes', '1 month', 5)
    )

    if not rows:
        return

    return [article['name'] for article in rows]


def insert_articles(from_article, to_articles):
    """Updates the database with article name and its' contained articles.
    """

    article_placeholders = ', '.join(['(%s)'] * len(to_articles))

    if not CONNECTION.non_query(
            'INSERT INTO article (name) '
            'VALUES {} '
            'ON CONFLICT DO NOTHING;'.format(article_placeholders),
            to_articles):
        return

    values = []

    for link in to_articles:
        values.append(from_article)
        values.append(link)

    link_placeholders = ', '.join(['(%s, %s)'] * len(to_articles))

    if not CONNECTION.non_query(
            'INSERT INTO link (from_article, to_article) '
            'VALUES {} '
            'ON CONFLICT ON CONSTRAINT u_constraint DO NOTHING;'.format(link_placeholders),
            values):
        return

    return CONNECTION.non_query(
        'UPDATE article '
        'SET last_crawled = NOW() '
        'WHERE name = %s;',
        [from_article])


def delete(article):
    """Delete an article from the database.
    """
    
    return CONNECTION.non_query(
        'DELETE FROM link '
        'WHERE to_article = %s;'
        'DELETE FROM article '
        'WHERE name = %s;',
        [article, article])


def crawler():
    """The crawlers' main function where it asks for articles and populates the database.
    """

    crawler_id = uuid.uuid4()

    while True:
        articles_to_crawl = get_articles(crawler_id)
        LOG.warning('{} got articles {}'.format(crawler_id, articles_to_crawl))

        if not articles_to_crawl:
            time.sleep(1)
            continue

        for article in articles_to_crawl:
            article_links = wikipedia.Article(article).links
            if article_links:
                insert_articles(article, article_links)
            else:
                delete(article)


if __name__ == '__main__':
    while True:
        try:
            crawler()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as exc:
            LOG.error(exc)

