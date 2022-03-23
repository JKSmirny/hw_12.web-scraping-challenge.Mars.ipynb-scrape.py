from flask import Flask, redirect, render_template
import scrape_mars
from flask_pymongo import PyMongo 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create route that renders index.html template
@app.route("/scrape")
def indexxx():
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    newvalues = { "$set": mars_data }
    mars.update_one({}, newvalues, upsert=True)
    return redirect("/", code=302)   

@app.route("/")
def index():
    mars_dict = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)    
if __name__ == "__main__":
    app.run(debug=True, port=8000)