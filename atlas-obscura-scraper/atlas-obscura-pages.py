import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import sys

# note: recommended not to retrieve more than 10 countries in one run

# example run command: <python3 atlas-obscura-pages.py 0 1 algeria.csv> where 0 is the index to
# start at and 1 is the index to end at. this command would return data for only algeria.
# algeria.csv is the name and location of the output file.

# load without images
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

# our web driver
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)


# given a link to a country's page, returns a list of attraction links
def links_from_country(driver, link):
    driver.get('https://www.atlasobscura.com' + link+'/places')
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    results = []
    for card in soup.find_all("div", {"class": "CardWrapper"}):
        if card.find('a', href=True):
            a = card.find('a', href=True)
            results.append(a['href'])

    print(results)
    return results


# given the link to an attraction, returns the description
def get_description(driver, a_link):
    driver.get('https://www.atlasobscura.com' + a_link)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    description = ""

    # retrieve main body
    body1 = soup.find("div", {"id": "place-body"})
    if body1:
        for p in body1.find_all("p"):
            description = description + " " + p.text.strip().replace('\xa0', ' ')

    # retrieve "Know Before You Go" section
    body2 = soup.find("div", {"class": "DDP__direction-copy"})
    if body2:
        for p in body2.find_all("p"):
            description = description + " " + p.text.strip().replace('\xa0', ' ')

    # print(description)
    return description.strip()


# given a link to a country's page, returns a list with each attraction's information
# as [attraction_name, attraction_location, attraction_blurb]
def info_from_country(driver, country_link):
    full_link = 'https://www.atlasobscura.com' + country_link+'/places'
    driver.get(full_link)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    results = []
    for card in soup.find_all("div", {"class": "Card__content-wrap"}):
        # retrieve attraction_location
        location = card.find("div", {"class": 'Card__hat'}).text.strip()
        attraction = card.find('h3').text.strip()  # retrieve attraction_name
        blurb = card.find(
            "div", {"class": "Card__content"}).text.strip()  # retrieve attraction_blurb

        info = [attraction, location, blurb]
        print(info)
        results.append(info)

    # print(results)
    return results


# given a link to a country's page, gets all of the attraction entries for that country
# as [attraction_name, attraction_location, attraction_blurb, attraction_url, attraction_desc]
def get_country_data(driver, country_link):
    attraction_links = links_from_country(driver, country_link)
    entries = info_from_country(driver, country_link)

    index = 0
    for a_link in attraction_links:
        description = get_description(driver, a_link)
        entries[index].append('https://www.atlasobscura.com' + a_link)
        entries[index].append(description)
        index += 1
    return entries


# gets a list of all country page links from https://www.atlasobscura.com/destinations
def get_country_links(driver):
    driver.get('https://www.atlasobscura.com/destinations')
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    results = []
    container = soup.find("section", {"class": "ao-container-padded"})
    for li in container.find_all("li"):
        if li.find('a', href=True):
            a = li.find('a', href=True)
            results.append(a['href'])

    return results


# get run arguments
start_index = int(sys.argv[1])
end_index = int(sys.argv[2])
output_file = str(sys.argv[3])

# get country links for specified range of indices
country_links = get_country_links(driver)
sample_data = country_links[start_index:end_index]

# get entries
output = []
for country_link in sample_data:
    entries = get_country_data(driver, country_link)
    for entry in entries:
        output.append(entry)

# creating headers, outputting file
header = ["attraction", "location", "blurb", "url", "description"]
pd.DataFrame(output).to_csv(output_file, index_label="index", header=header)
