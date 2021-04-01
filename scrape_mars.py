# Dependencies and setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
from flask import Flask, render_template
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import requests
import pymongo

# Define scrape function
def scrape():

    # Initialize browser/set up Splinter (this needs work with tutor)
    executable_path = {"executable_path": "/Users/matth/.wdm/drivers/chromedriver/win32/89.0.4389.23"}
    # executable_path = {"executable_path":ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless = False)

    # NASA Mars News -----------------------------------------------------------------

    # URL of page to be scraped
    newsURL = "https://redplanetscience.com"
    browser.visit(newsURL)

    # Loop through homepage (this works from class example but maybe only one loop is needed?  ask tutor)
    for x in range(1):
    
        # HTML object
        html = browser.html
    
        # Parse HTML with BeautifulSoup
        soup = bs(html, "html.parser")
    
        # Retrieve all elements that contain News Titles and Paragraph Text
        articles = soup.find_all("div", class_ = "list_text")
    
        # Iterate through each headline
        for article in articles:
        
            # Use BeautifulSoup's find() method to navigate and retrieve attributes
            newsTitle = article.find("div", class_ = "content_title").text
            paragraphText = article.find("div", class_ = "article_teaser_body").text
            print("------------------------------------------")
            print(f"Article:  {newsTitle}")
            print(f"Teaser:  {paragraphText}")
            print(" ")
            print(f"Mars News Scraping Complete.")
    
    # JPL Mars Space Images - Featured Image ------------------------------------------

    # URL of page to be scraped
    imageURL = "https://spaceimages-mars.com/"
    browser.visit(imageURL)

    # HTML object
    imageHTML = browser.html
    
    # Parse HTML with BeautifulSoup
    imageSoup = bs(imageHTML, "html.parser")

    # Find href within anchor tag element
    featuredImage = imageSoup.find("a", class_ = "showimg fancybox-thumbs")["href"]

    # Declare variable and combine main URL with link
    featured_image_url = f"https://spaceimages-mars.com/{featuredImage}"
    print(f"Featured Image URL:  {featured_image_url}")
    print(" ")
    print(f"JPL Mars Space Images - Featured Image Scraping Complete.")

    # Mars Facts ----------------------------------------------------------------------

    # Use the read_html function in pandas to automatically scrape tabular data
    tableURL = "https://galaxyfacts-mars.com"
    tables = pd.read_html(tableURL)

    # Slice off DataFrame that we want using normal indexing
    marsFacts_df = tables[0]

    # Export DataFrame to HTML
    marsFacts_df.to_html("Resources/DataFrame.html", index = False)

    # Extract first row from DataFrame and set it as the header
    new_header = marsFacts_df.iloc[0]
    marsFacts_df = marsFacts_df[1:]
    marsFacts_df.columns = new_header

    print(f" ")
    print(f"Mars Facts Scraping Complete.")

    # Mars Hemispheres ----------------------------------------------------------------

    # URL of page to be scraped
    hemispheresURL = "https://marshemispheres.com/"
    browser.visit(hemispheresURL)

    # HTML object
    hemispheresHTML = browser.html
    
    # Parse HTML with BeautifulSoup
    hemispheresSoup = bs(hemispheresHTML, "html.parser")
    
    # Retrieve all elements that contain image URLs to the full resolution image
    links = hemispheresSoup.find_all("div", class_ = "description")

    # Create empty list to be appended with dictionaries
    hemisphere_image_urls = []

    # Iterate through each description
    for link in links:
        
        # Use BeautifulSoup's find() method to navigate and retrieve attributes
        imageTitle = link.find("h3").text
        imageLink = link.find("a", class_ = "itemLink product-item")["href"]
    
        # Visit the link with the full resolution image
        browser.visit(hemispheresURL + imageLink)
    
        # HTML object
        linkHTML = browser.html
    
        # Parse HTML with BeautifulSoup
        linkSoup = bs(linkHTML, "html.parser")
    
        # Full resolution image URL
        fullURL = hemispheresURL + linkSoup.find("img", class_ = "wide-image")["src"]
    
        # Append to list of dictionaries
        hemisphere_image_urls.append({"title":imageTitle, "img_url":fullURL})
    
        # Display titles and links
        print("------------------------------------------")
        print(f"Title:  {imageTitle}")
        print(f"Link:   {fullURL}")

    # Display end statement    
    print(" ")
    print("Mars Hemispheres Scraping Complete.")

    # Close remote browser
    browser.quit()

    # All Pages Data ------------------------------------------------------------------

    # Return one Python dictionary containing all of the scraped data
    scrapedData = {
        "News_Title":newsTitle, "News_Text":paragraphText,
        "Featured_Image":featured_image_url,
        "Mars_Facts":marsFacts_table,
        "Hemisphere_Images":hemisphere_image_urls
    }

    # Return dictionary
    return scrapedData