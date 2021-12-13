# Import dependancies 
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pymongo 
import requests
import pandas as pd
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager

#Set up Splinter
def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
#Scrape 1
    url1 = 'https://redplanetscience.com/'
    browser.visit(url1)
    html=browser.html
    soup = bs(html, 'html.parser')
    news1head = soup.find_all('div', class_='content_title')[0].text
    new1con = soup.find_all('div', class_='article_teaser_body')[0].text

#Scrape 2
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = soup.find("img", {"class": "headerimage"})['src']
    final_image = (url2 + featured_image_url)

#Scrape 4
    url3 = 'https://galaxyfacts-mars.com/'
    browser.visit(url3)
    mars_table = pd.read_html(url3)
    table1= mars_table[1]
    table2 = table1.to_html(index=False)
    #table1.to_html("Table.html", index=False)

    #table1.to_html("Table.html", index=False)

#Scrape 5
    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)
    html = browser.html
    soup = bs(html, 'html.parser')
    marshemispheres = soup.find_all("div", {"class":"item"})

    hemisphere = []
    for x in marshemispheres:
        ref = url4 + x.find("a", {"class": "itemLink"})["href"]
        browser.visit(ref)
        time.sleep(1)
    
        html = browser.html
        soup = bs(html, "html.parser")
    
        img_url = url4 + soup.find("img", {"class", "wide-image"})["src"]
        title = soup.find("h2", {"class", "title"}).text
    
        images_title = {title:img_url}
    
        hemisphere.append(images_title)

# Store Data in Dictionary
    mars_data_dict={
        "news1head":news1head,
        "new1con":new1con,
        "final_image":final_image,
        "table2":table2,
        "hemisphere":hemisphere
    }

# Close the browser after scraping 
    browser.quit()
# Return Results 
    return mars_data_dict


