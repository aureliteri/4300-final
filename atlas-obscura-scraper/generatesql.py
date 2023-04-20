import json

# Load JSON file
with open('atlas-obscura-pages-full.json', 'r') as f:
    data = json.load(f)

# Define MySQL script filename
mysql_script_filename = 'data.sql'

# Open MySQL script file
with open(mysql_script_filename, 'w') as f:

    # Create atlasfull table
    # create_table_statement = """CREATE TABLE atlasfull (
    #                             id INT PRIMARY KEY AUTO_INCREMENT,
    #                             index BIGINT,
    #                             attraction VARCHAR(255),
    #                             location VARCHAR(255),
    #                             blurb VARCHAR(255),
    #                             url VARCHAR(255),
    #                             description VARCHAR(7000),
    #                             tags VARCHAR(255),
    #                             lemmatized_description VARCHAR(7000)
    #                           );\n"""
    # f.write(create_table_statement)

    # Generate MySQL insert statement for all data
    values = []
    for item in data:
        values.append("({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}')\n".format(
            item['index'],
            item['attraction'].replace("'", "''").replace("\n", " "),
            item['location'].replace("'", "''").replace("\n", " "),
            item['blurb'].replace("'", "''").replace("\n", " "),
            item['url'].replace("'", "''").replace("\n", " "),
            item['description'].replace("'", "''").replace("\n", " "),
            item['tags'].replace("'", "''").replace("\n", " "),
            item['lemmatized_description'].replace("'", "''").replace("\n", " ")
        ))

    insert_statement = "INSERT INTO atlasfull (index, attraction, location, blurb, url, description, tags, lemmatized_description) VALUES \n{};\n".format(",".join(values))

    # Write insert statement to MySQL script file
    f.write(insert_statement)
