#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
import requests
import urllib
from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin
from urllib.parse import urlsplit
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time 
from bs4 import BeautifulSoup as yourVariable

#preparation steps:
import pymongo
#install flask
from flask import Flask, render_template

# setup mongo connection (MongoDB Compass to python)
conn = "mongodb://localhost:27017" # the default port for MongoDB
client = pymongo.MongoClient(conn) #to connect to Mongo database via db = client.name_of_database (it'll be created if absent)

# connect to mongo db and collection
db = client.hemispheresDB
collection = db.collection

### NASA Mars News
   
##Connecting to Mars Space News Site site
url_space = "https://spacenews.com/segment/news"
# Retrieve page with the requests module
response = requests.get(url_space)

def scrape():
    from webdriver_manager.chrome import ChromeDriverManager
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # Create BeautifulSoup object; parse with 'lxml'
    from bs4 import BeautifulSoup as bs
    soup = bs(response.text, 'lxml')

    mars_dict = {}
        
    #find the latest articles, search for a title
    results = soup.find_all('div', class_='article-item__top')
    for result in results: 
        title = result.find('a', class_='title').text
            
    # Extract title text, save it into variable
    news_title = soup.title.text
    mars_dict['a_title'] = news_title

    paragraphs = soup.find_all("div", class_="article-meta")
    for paragraph in paragraphs: 
        news_paragraph = paragraph.find('p', class_='post-excerpt').text
    mars_dict['b_paragraph'] = news_paragraph 

    from webdriver_manager.chrome import ChromeDriverManager
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    #Visit the url for the Featured Space Image site (https://spaceimages-mars.com), assign the url string to a variable
    space_image = "https://spaceimages-mars.com"
    browser.visit(space_image)
    time.sleep(2)

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(space_image))
    
    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    
    # Create BeautifulSoup object; parse with 'parser'
    from bs4 import BeautifulSoup as bs
    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    soup = bs(urlopen(space_image))

    for img in soup.find_all('img'):
        featured_image_url = urljoin(space_image, img['src'])
        file_name = img['src'].split('/')[-1]
        urlretrieve(featured_image_url, file_name)

        mars_dict['c_featured_image'] = featured_image_url
        mars_dict['d_featured_image_name'] = file_name 

    ### Mars Facts

    url_facts = 'https://galaxyfacts-mars.com/'
    time.sleep(2)
    table = pd.read_html(url_facts)

    facts_table = table[0]
    facts_table.columns = ["Description", "Mars", "Earth"]
    facts_table.set_index("Description", inplace=True)

    mars_dict["e_Mars_data_table"] = facts_table.to_html()

    ### Mars Hemispheres

    mars_hemispheres_list = []
    #Visit the url for Mars Hemispheres site (https://marshemispheres.com/), assign the url string to a variable
    hemisphere_images = "https://marshemispheres.com/"
    browser.visit(hemisphere_images)

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(space_image))
    
    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    
    # Create BeautifulSoup object; parse with 'parser'
    from bs4 import BeautifulSoup as bs
    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, 'html.parser')
    
    #Visit the url for Mars Hemispheres site (https://marshemispheres.com/), assign the url string to a variable
    hemisphere_images = "https://marshemispheres.com/"
    browser.visit(hemisphere_images)

    mars_hemispheres_list = []
    soup = bs(urlopen(hemisphere_images))

    for i in range (4):
        time.sleep(5) #to create a loop
        # locate tag h3 (corresponding hemispheres)
        images = browser.find_by_tag("h3")
        # click on each image to get url
        images[i].click()
        # separate url
        html = browser.html
        soup = bs(html, "html.parser")
        # search for HD image
        url_hemisphere = soup.find("img", class_="wide-image")["src"]
        # looking for image title
        img_title = soup.find("h2",class_="title").text
        # get image url
        img_url = "https://marshemispheres.com/"+ url_hemisphere
        # store the results into dictionary
        dictionary={"title":img_title,"img_url":img_url}
        # append the dictionary into mars hemisheres list
    mars_hemispheres_list.append(dictionary)
    browser.back()
    mars_dict['f_Mars_hemispheres_list'] = mars_hemispheres_list

    return mars_dict
    




