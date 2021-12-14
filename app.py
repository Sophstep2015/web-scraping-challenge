from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    #mars_data_dict = mongo.db.mars_data_dict.insert_one()
    mars_data_dict = mongo.db.mars_data_dict.find_one()
    #mars_data_dict = mongo.db.mars_data_dict.find_one()
    return render_template("index.html", mars_data_dict=mars_data_dict)
 
@app.route("/scrape")
def scrape():
    mars_data_dict = mongo.db.mars_data_dict
    mars_data = scrape_mars.scrape_all()
    mars_data_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run()