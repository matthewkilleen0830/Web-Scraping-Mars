# Dependencies and setup
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create instance of Flask app
app = Flask(__name__)

# Initialize PyMongo to work with MongoDBs (this needs work with tutor)
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
marsData = mongo.db.marsData

# Create route that renders index.html template
@app.route("/")
def index():
    return render_template("index.html")

# Create a route called /scrape that will import your scrape_mars.py script and call your scrape function
@app.route("/scrape")
def scrape():

    # Call scrape function
    scrapedData = scrape_mars.scrape()

    # Update MongoDB with scraped data
    marsData.update({}, scrapedData, upsert = True)

    # Redirect to landing page
    return redirect("/index.html)

# Define main behavior
if __name__ == "__main__":
    app.run(debug = True)