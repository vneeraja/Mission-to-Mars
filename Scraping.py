
# import splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # set up the execuatble path
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    news_title, news_paragraph = mars_news(browser)

     # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser),
    }
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)


    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # set up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title,news_p

def featured_image(browser):
    # Featured Images
    # Visit URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


    # set up HTML parser
    html = browser.html
    image_soup = soup(html, 'html.parser')


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel

    except AttributeError:
        return None, None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    try:
        # Scrape Mars Facts
        # Read the table containing Mars facts
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
      return None

    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html()

def mars_hemispheres(browser):
        # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

    # Hemispheres

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.item', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    mars_soup = soup(html, 'html.parser')


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    Img_and_titles = mars_soup.find_all('div', class_="item")

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for img_and_title in Img_and_titles:
    
        # Create an empty dictionary
        hemispheres = {}
        
        link = img_and_title.find('h3')
        img_link = browser.find_by_text(link.text)
        img_link.click()
        
        html = browser.html
        img_soup = soup(html, 'html.parser')
        title = img_soup.find('h2').text
        
        # Retrieve the full image urls
        hemp_img = img_soup.find('div', class_='downloads')
        hemp_full_img = hemp_img.find('a')['href']
        hemp_full_img_url = url + hemp_full_img
        
        hemispheres = {"img_url":hemp_full_img_url, "title":title}
        hemisphere_image_urls.append(hemispheres)
        browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

