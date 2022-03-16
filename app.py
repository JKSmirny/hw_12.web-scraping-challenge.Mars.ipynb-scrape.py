#!/usr/bin/env python
# coding: utf-8

# In[1]:


###Mission to Mars

# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import pymongo
import os
from flask import Flask, render_template, redirect
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.webdriver.common.keys import Keys

#Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

#preparation steps:
import pymongo
#install flask
from flask import Flask, render_template
app = Flask(__name__)

# setup mongo connection (MongoDB Compass to python)
conn = "mongodb://localhost:27017" # the default port for MongoDB
client = pymongo.MongoClient(conn) #to connect to Mongo database via db = client.name_of_database (it'll be created if absent)

# connect to mongo db and collection
db = client.name_of_database
collection = db.collection

### NASA Mars News

##Connecting to Mars Space News Site site
url_space = "https://spacenews.com/"
# Retrieve page with the requests module
response = requests.get(url_space)

# Create BeautifulSoup object; parse with 'lxml'
from bs4 import BeautifulSoup as bs
soup = bs(response.text, 'lxml')

#find the latest articles, search for a title
results = soup.find_all('div', class_='article-item__top')
for result in results: 
     title = result.find('a', class_='title').text
   
# Extract title text, save it into variable
news_space_title = soup.title.text
print(news_space_title)

# Print all the paragraph texts, save it into variable
paragraphs_space = soup.find_all('p')
for news_space_paragraph in paragraphs_space:
    print(news_space_paragraph.text)

##Connecting to Mars Space News Site site
url_red = "https://redplanetscience.com/"
# Retrieve page with the requests module
response = requests.get(url_red)

# Create BeautifulSoup object; parse with 'lxml'
from bs4 import BeautifulSoup as bs
soup = bs(response.text, 'lxml')

#find the latest articles, search for a title
results = soup.find_all('div', class_='article-item__top')
for result in results: 
     title = result.find('a', class_='title').text
      
# Extract title text, save it into variable
news_red_title = soup.title.text
print(news_red_title)

# Print all the paragraph texts, save it into variable
paragraphs_red = soup.find_all('p')
for news_red_paragraph in paragraphs_red:
    print(news_red_paragraph.text)

### JPL Mars Space Images - Featured Image

#intial preparations
from webdriver_manager.chrome import ChromeDriverManager

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

import urllib
from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin

#Visit the url for the Featured Space Image site (https://spaceimages-mars.com), assign the url string to a variable
url = "https://spaceimages-mars.com"

soup = bs(urlopen(url))

for img in soup.find_all('img'):
    featured_image_url = urljoin(url, img['src'])
    file_name = img['src'].split('/')[-1]
    urlretrieve(featured_image_url, file_name)
    print(featured_image_url)

### Mars Facts

#use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

import pandas as pd

url = 'https://galaxyfacts-mars.com/'
tables = pd.read_html(url)
tables

#Use Pandas to convert the data to a HTML table string
type(tables)

facts_df = tables[0]
facts_df.head()

#Use Pandas to convert the data to a HTML table string.
Mars_facts = facts_df.drop(index=0)
Mars_facts = Mars_facts.rename(columns={0:'Data_name', 1: 'Mars_data', 2 : 'Earth data'})
Mars_facts.head()

Mars_facts.to_html("data_Mars_facts.html")

### Mars Hemispheres

#Visit the astrogeology site (https://marshemispheres.com/) to obtain high resolution images for each of Mars' hemispheres.
astropedia_url = 'https://marshemispheres.com/'
#click each of the links to the hemispheres in order to find the image url for the full resolution image.

cerberus = 'https://marshemispheres.com/images/cerberus_enhanced.tif'
    #images/cerberus_enhanced.tif
#https://marshemispheres.com/cerberus.html

schiaparelli = 'https://marshemispheres.com/images/schiaparelli_enhanced.tif'
    #images/schiaparelli_enhanced.tif  
#https://marshemispheres.com/schiaparelli.html

syrtis_major = 'https://marshemispheres.com/images/syrtis_enhanced.tif'
    #images/syrtis_enhanced.tif
#https://marshemispheres.com/syrtis.html

valles_marineris = 'https://marshemispheres.com/images/valles_enhanced.tif'
    #images/valles_enhanced.tif
#https://marshemispheres.com/valles.html

#Save both the image url string for the full resolution hemisphere image
#and the Hemisphere title containing the hemisphere name. 
#Use a Python dictionary to store the data using the keys `img_url` and `title`

hemisphere_image_dict = [
    
    {"title": "Cerberus Hemisphere", "img_url": "https://marshemispheres.com/images/cerberus_enhanced.tif"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://marshemispheres.com/images/schiaparelli_enhanced.tif"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://marshemispheres.com/images/syrtis_enhanced.tif"},
    {"title": "Valles Marineris Hemisphere", "img_url": "https://marshemispheres.com/images/valles_enhanced.tif"}
]


# In[47]:


hemisphere_image_dict


# In[48]:


#Append the dictionary with the image url string and the hemisphere title to a list. 
#This list will contain one dictionary for each hemisphere.
hemisphere_list = []
hemisphere_list.append(hemisphere_image_dict)
print(hemisphere_list)


# In[107]:


## Step 2 - MongoDB and Flask Application

#Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

#* Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

#* Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.

#* Store the return value in Mongo as a Python dictionary.

#* Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.

#* Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.

#![final_app_part1.png](Images/final_app.png)

#Use MongoDB with Flask templating to create a new HTML page
#that displays all of the information that was scraped from the URLs above
# The default port used by MongoDB is 27017
# https://docs.mongodb.com/manual/reference/default-mongodb-port/
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define the 'hemisphere_db' database in Mongo
db = client.hemisphere_db
hemisphere_list = db.hemisphere_list

# Insert a document into the 'hemisphere' collection
db.hemisphere_list.insert_one(
 {'title': 'Cerberus Hemisphere',
  'img_url': 'https://marshemispheres.com/images/cerberus_enhanced.tif'}
),
db.hemisphere_list.insert_one(
 {'title': 'Schiaparelli Hemisphere',
  'img_url': 'https://marshemispheres.com/images/schiaparelli_enhanced.tif'}
),
db.hemisphere_list.insert_one(
 {'title': 'Syrtis Major Hemisphere',
  'img_url': 'https://marshemispheres.com/images/syrtis_enhanced.tif'}
),
db.hemisphere_list.insert_one(
 {'title': 'Valles Marineris Hemisphere',
  'img_url': 'https://marshemispheres.com/images/valles_enhanced.tif'}
)

# query the hemispheres' collection
hemisphere = db.hemisphere_list.find()

browser.quit()

#return hemisphere_dict

if __name__ == "__main__":
    app.run(debug=True)

## Step 3 - Submission

#To submit your work to BootCampSpot, create a new GitHub repository and upload the following:

#1. The Jupyter Notebook containing the scraping code used.

#2. Screenshots of your final application.

#3. Submit the link to your new repository to BootCampSpot.

#4. Ensure your repository has regular commits and a thorough README.md file
