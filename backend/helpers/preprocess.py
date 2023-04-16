import json
import string
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

with open('/Users/amyouyang/Documents/Cornell/Senior/CS4300/4300-final/atlas-obscura-scraper/pages-run/merged-pages.json', 'r') as infile:
    input_array = json.load(infile)

arr = []

count = 0
for dictionary in input_array:
    dictionary['index'] = count
    count += 1
    description_value = dictionary['description']
    description_value = description_value.translate(
        str.maketrans('', '', string.punctuation))
    words = description_value.split()
    lemmatized_description_value = ' '.join(
        [lemmatizer.lemmatize(word) for word in words])

    dictionary['lemmatized_description'] = lemmatized_description_value
    arr.append(dictionary)

with open('/Users/amyouyang/Documents/Cornell/Senior/CS4300/4300-final/atlas-obscura-scraper/atlas-obscura-pages-full.json', 'w') as outfile:
    json.dump(arr, outfile)
