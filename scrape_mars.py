# Dependencies and setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
from flask import Flask, render_template
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

# Define scrape function
def scrape():

    # Initialize browser/set up Splinter
    executable_path = {"executable_path":ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless = False)

    # NASA MARS NEWS -----------------------------------------------------------------

    # URL of page to be scraped
    newsURL = "https://redplanetscience.com"
    browser.visit(newsURL)
    time.sleep(1)
    
    # Declare variables to store scraped Title and Teaser 
    newsTitle = browser.find_by_css(".content_title")[0].text
    paragraphText = browser.find_by_css(".article_teaser_body")[0].text

    # JPL MARS SPACE IMAGES - FEATURED IMAGE ------------------------------------------

    # URL of page to be scraped
    imageURL = "https://spaceimages-mars.com/"
    browser.visit(imageURL)
    time.sleep(1)

    # HTML object
    imageHTML = browser.html
    
    # Parse HTML with BeautifulSoup
    imageSoup = bs(imageHTML, "html.parser")

    # Find href link within anchor tag element
    featuredImage = imageSoup.find("a", class_ = "showimg fancybox-thumbs")["href"]

    # Declare variable and combine main URL with link
    featured_image_url = (f"https://spaceimages-mars.com/{featuredImage}")

    # MARS FACTS ----------------------------------------------------------------------

    # Use the read_html function in pandas to automatically scrape tabular data
    tableURL = "https://galaxyfacts-mars.com"
    marsTable = pd.read_html(tableURL)

    # Slice off DataFrame that we want using normal indexing
    marsFacts_df = marsTable[0]

    # Extract first row from DataFrame and set it as the header
    new_header = marsFacts_df.iloc[0]
    marsFacts_df = marsFacts_df[1:]
    marsFacts_df.columns = new_header

    # Export DataFrame to HTML
    marsFacts_table = marsFacts_df.to_html()

    # MARS HEMISPHERES ----------------------------------------------------------------

    # URL of page to be scraped
    hemispheresURL = "https://marshemispheres.com/"
    browser.visit(hemispheresURL)
    time.sleep(1)

    # Create empty list to be appended with dictionary
    hemisphere_image_urls = []

    # Declare variable to store scraped links
    imageLinks = browser.find_by_css("a.itemLink img")

    # Iterate through each page and scrape links
    for link in range(len(imageLinks)):
        
        # Create empty dictionary
        imageDict = {}

        # Locate and follow each subsequent link
        browser.find_by_css("a.product-item img")[link].click()

        # Declare variable to store scraped image URL
        image = browser.links.find_by_text("Sample").first

        # Append scraped image URL and scraped Title to dictionary
        imageDict["img_url"] = image["href"]
        imageDict["title"] = browser.find_by_css("h2.title").text
        
        # Append list with scraped dictionary
        hemisphere_image_urls.append(imageDict)
        
        # Go back
        browser.back()

    # ALL PAGES DATA ------------------------------------------------------------------

    # Create and append single dictionary with all scraped data
    scrapedData = {
    "News_Title":newsTitle, 
    "News_Text":paragraphText,
    "Featured_Image":featured_image_url,
    "Mars_Facts":marsFacts_table,
    "Hemisphere_Images":hemisphere_image_urls
    }

    # Close remote browser
    browser.quit()

    return scrapedData