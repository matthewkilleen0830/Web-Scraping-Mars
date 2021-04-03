# Dependencies and setup
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask app
app = Flask(__name__)

# Initialize PyMongo to work with MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsData"
mongo = PyMongo(app)

# Create route that renders index.html template
@app.route("/")
def index():
    collection = mongo.db.collection.find_one()
    return render_template("index.html", collection = collection)

# Create a route called /scrape that will import scrape_mars.py script and call scrape function
@app.route("/scrape")
def scrape():
    
    # Define collection within marsData db in MongoDB
    collection = mongo.db.collection

    # Call scrape function
    scrapedData = scrape_mars.scrape()
    print(scrapedData)

    # Update MongoDB collection with scraped data
    collection.update({}, scrapedData, upsert = True)

    # Redirect to landing page
    return redirect("/", code = 302)

# Define main behavior
if __name__ == "__main__":
    app.run(debug = True)