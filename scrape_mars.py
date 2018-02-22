
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import pymongo
from selenium import webdriver




def init_browser():
    #executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", headless=False)
    
        
def scrape():
    browser = init_browser()
    mars_data = {}


    # Mars News
       
    NASANewsurl = 'https://mars.nasa.gov/news/'
    browser.visit(NASANewsurl)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    NASANews = soup.find("div", class_="content_title")
    news_title = NASANews.find('a').text

    news_para = soup.find("div", class_="rollover_description_inner").text

    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_para



    # JPL Mars Space Image - Featured Image

    
   
    spaceimageurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(spaceimageurl)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

    browser.click_link_by_partial_text('more info')
    time.sleep(2)

    jpl_html = browser.html
    spaceimage = BeautifulSoup(jpl_html, 'html.parser')

    featured_image = spaceimage.find('figure', class_='lede').find('img')['src']
    
    large_image_url = "https://www.jpl.nasa.gov"+featured_image

    mars_data['featured_image_url'] = large_image_url



    # Mars Weather

    marsweatherurl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(marsweatherurl)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    marsweather = soup.find('div', class_='js-tweet-text-container')
    mars_weather = marsweather.find('p', class_='TweetTextSize').text
    
    mars_data['mars_weather'] = mars_weather


    
    # Mars facts

    marsfactsurl = 'https://space-facts.com/mars/'
    marstables = pd.read_html(marsfactsurl)
    marsdf = marstables[0]
    marsdf.columns = ['Description', 'Value']
    #marsdf.set_index('Description', inplace=True)
    mars_table = marsdf.to_html(index = False)
  
    mars_data['mars_facts'] = mars_table
    
        
    
    # Mars Hemisperes


    marshemurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(marshemurl)

    marshtml = browser.html
    soup = BeautifulSoup(marshtml, 'html.parser')

    hemispheres = soup.find_all('div', class_="description")
    
    hemisphere_image_url = []
    base_url = 'https://astrogeology.usgs.gov'

    for hemisphere in hemispheres:
        imagetitle = hemisphere.h3.text
        hemurl = base_url + hemisphere.a['href']
          
        browser.visit(hemurl)  
        time.sleep(5)
        imagehtml = browser.html
        soup = BeautifulSoup(imagehtml, 'html.parser')
        imageurl = soup.find('div', class_='downloads').find('li').a['href']
           
        hemisphere_dict = {}
        hemisphere_dict = {'title' : imagetitle, 'img_url' : imageurl}
                     
        #append dictionary
        hemisphere_image_url.append(hemisphere_dict)
        
        browser.back()
    mars_data["hemispheres"] = hemisphere_image_url
    print(mars_data)
    return mars_data
