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

3. Create the database using the command 'python create_db.py'

4. Run as many crawlers as you like to populate the database `python crawler.py`.


## Usage

1. Run the Flask server in the terminal `python wiki_server.py`.

2. Connect to your local host in your browser `localhost:5000` and search.


Wiki Find can also retrieve the links contained in a specific article and the search function is case insensitive. Articles titles must be typed as they appear on Wikipedia, any typos or incomplete article titles will not work. 

For optimal performance it is best to make sure that the database is heavily populated to increase the chances that your desired articles have been crawled.
