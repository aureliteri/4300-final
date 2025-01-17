import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from helpers.PartOne import *
from helpers.PartTwo import *

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = ""
MYSQL_PORT = 4534
MYSQL_DATABASE = "travellocomotion_db"
# MYSQL_USER = "root"
# MYSQL_USER_PASSWORD = ""
# MYSQL_PORT = 3306
# MYSQL_DATABASE = ""

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded,
# but if you decide to use SQLAlchemy ORM framework,
# there's a much better and cleaner way to do this
# def sql_search(episode):
#     query_sql = f"""SELECT * FROM episodes WHERE LOWER( title ) LIKE '%%{episode.lower()}%%' limit 10"""
#     keys = ["id","title","descr"]
#     data = mysql_engine.query_selector(query_sql)
#     return json.dumps([dict(zip(keys,i)) for i in data])


def sql_search(table_name):
    query_sql = f"""SELECT * FROM {table_name}"""
    keys = ["index", "attraction", "location", "blurb",
            "url", "description", "tags", "lemmatized_description"]
    # keys = ["index", "description", "lemmatized_description",
    #         "url", "attraction", "location", "blurb"]
    data = mysql_engine.query_selector(query_sql)
    return [dict(zip(keys, i)) for i in data]


data = sql_search('atlas_data')
partOne = PartOne(data, 5000)
partTwo = PartTwo(partOne._tfidf_vec,
                  partOne._array_with_country,
                  partOne._attraction_by_token,
                  partOne._index_to_vocab, data)


def generate_tags(countries):
    tag_dict = partOne.generate_tags([countries])
    print(tag_dict, type(tag_dict))
    return tag_dict


@app.route("/country-list")
def country_list():
    print("form submitted")
    country_set = set()
    for entry in partOne._array_with_country:
        country_set.add(entry["country"])
    print(country_set)
    return list(country_set)


@app.route("/countries")
def get_countries():
    countries = request.args.get("countries")
    tags_dict = generate_tags(countries)
    tags = tags_dict[countries]
    print(tags)
    return tags


@app.route("/output")
def generate_output():
    tags = request.args.get("tags")
    pos = request.args.get("pos")
    neg = request.args.get("neg")

    pos = pos.strip().split(",")
    neg = neg.strip().split(",")
    tags = tags.strip().split(",")
    output_tuple = partTwo.get_top_attractions_w_neg(partTwo.pmi, pos, neg)
    output = [(location, url) for score, location, url in output_tuple]
    print(output)
    return output


@app.route("/home")
def home():
    return render_template('base.html', title="home")


@app.route("/")
def landing():
    return render_template('landing.html', title="landing")


# app.run(debug=True)