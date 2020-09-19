# Import dependencies
# Use Flask to render a template
from flask import Flask, render_template
# Use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
# To use our scraping code, we will convert from Jupyter notebook to Python
import scraping

# Set up Flask 
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# Our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the html page.
# This route, @app.route("/"), tells Flask what to display when we're looking at the home page
@app.route("/")
def index():
    # Uses PyMongo to find the "mars" collection in our database
   mars = mongo.db.mars.find_one()
   # index.html (index.html is the default HTML file that we'll use to display the content we've scraped).
   # This means that when we visit our web app's HTML page, we will see the home page.
   # , mars=mars) tells Python to use the "mars" collection in MongoDB.
   return render_template("index.html", mars=mars)

# Set up scraping route
# This route will be the "button" of the web application, 
# the one that will scrape updated data when we tell it to from the homepage of our web app. 
# It'll be tied to a button that will run the code when it's clicked.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   # In this line, we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# Tell Flask to run
if __name__ == "__main__":
   app.run()