import json
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

with open('/Users/aaronkang/Desktop/current_semester/SP23/CS4300/4300-final/atlas-obscura-scraper/atlas-obscura-full.json', 'r') as infile:
    input_array = json.load(infile)

arr = []

for dictionary in input_array:

    description_value = dictionary['description']

    words = description_value.split()
    lemmatized_description_value = ' '.join([lemmatizer.lemmatize(word) for word in words])

    dictionary['lemmatized_description'] = lemmatized_description_value
    arr.append(dictionary)

with open('/Users/aaronkang/Desktop/current_semester/SP23/CS4300/4300-final/atlas-obscura-scraper/atlas-obscura-full-new.json', 'w') as outfile:
    json.dump(arr, outfile)

