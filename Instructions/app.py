from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/nasa_info"
mongo = PyMongo(app)

@app.route("/")
def index():
    nasa_info = mongo.db.nasa_info.find_one()
    return render_template("index.html", nasa_info=nasa_info)

@app.route('/scrape')
def scraper():
    nasa_info = mongo.db.nasa_info
    nasa_data = scrape_mars.scrape()
    nasa_info.update({}, nasa_data, upsert=True)
    return redirect("/", code=302)

    
if __name__ == "__main__":
    app.run(debug=True)