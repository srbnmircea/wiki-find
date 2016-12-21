"""A simple script to automate the Wiki database creation process."""

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import postgres


def create_db():
    """Create the Wiki database if there is none."""

    con = None
    con = connect(user='postgres')

    dbname = "wiki"

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('CREATE DATABASE ' + dbname)
    cur.close()
    con.close()

    connection = postgres.Connection('postgres', 'wiki')

    connection.non_query(
        'CREATE TABLE article ('
        '   name TEXT PRIMARY KEY,'
        '   last_crawled TIMESTAMP,'
        '   assigned_crawler_id UUID,'
        '   assigned_crawler_time TIMESTAMP'
        ');'
    )

    connection.non_query(
        'CREATE UNIQUE INDEX name_id ON article (lower(name));'
    )

    connection.non_query(
        'CREATE TABLE link ('
        '   from_article TEXT REFERENCES article (name),'
        '   to_article TEXT,'
        '   CONSTRAINT u_constraint UNIQUE (from_article, to_article)'
        ');'
    )

    connection.non_query(
        'INSERT INTO article (name) VALUES (\'Foobar\');'
    )

if __name__ == '__main__':
    create_db()
