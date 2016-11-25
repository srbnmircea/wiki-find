# Wiki Find

Wiki Find is a simple search engine that finds the minimum distance between two given Wikipedia articles using article links as unit of measurement.


## Dependencies

1. Python 3.5.1

2. [PostgreSQL 9.6](https://www.postgresql.org/download/)

3. [Psycopg 2.6.2](http://initd.org/psycopg/docs/install.html)

4. [Flask](http://flask.pocoo.org/docs/0.11/installation/)

5. [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)


## Up and Running

1. Install PostgreSQL, make sure to remove the password for the user postgres since that will be the user where the 'wiki' database will be created.

2. Create the 'wiki' database following the instructions below.

3. Run as many crawlers as you like to populate the database `python crawler.py`.


## Creating the database

While logged in as user 'postgres' create the 'wiki' database and connect to it.

```
CREATE DATABASE wiki;

\connect wiki;
```

Create the two 'article' and 'link' tables using the following code. In order to make the crawler run the 'article' database must be populated with at least one article of your choosing.


```
CREATE TABLE article (
    name TEXT PRIMARY KEY,
    last_crawled TIMESTAMP,
    assigned_crawler_id UUID,
    assigned_crawler_time TIMESTAMP
);

CREATE UNIQUE INDEX name_id ON article (lower(name));

CREATE TABLE link (
    from_article TEXT REFERENCES article (name),
    to_article TEXT,
    CONSTRAINT u_constraint UNIQUE (from_article, to_article)
);

INSERT INTO article (name) VALUES ('Foobar');
```


## Usage

1. Run the Flask server in the terminal `python wiki_server.py`.

2. Connect to your local host in your browser `localhost:5000` and search.


Wiki Find can also retrieve the links contained in a specific article and the search function is case insensitive. Articles titles must be typed as they appear on Wikipedia, any typos or incomplete article titles will not work. 

For optimal performance it is best to make sure that the database is heavily populated to increase the chances that your desired articles have been crawled.
