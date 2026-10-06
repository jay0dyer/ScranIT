from flask import Flask, render_template, request
from ScranSearch import ScranSearchEngine
import json
print("loading back end...")
engine = ScranSearchEngine()
app = Flask(__name__)

# READ BACKEND USAGE .TXT !!

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/', methods=['POST'])
def landing_page_search():
    text = request.form['text']
    result=engine.Search(text)

    return render_template("search.html", result=result, text = text)

@app.route('/search')
def search():
    return render_template('search.html') # this links us to the templates

@app.route('/search', methods=['POST'])
def search_form_post():
    text = request.form['text']
    sort = request.form['sortBy']
    print(f"Search Query: {text}")
    print(f"Sort Option: {sort}")
    result=engine.Search(text, sort)

    return render_template("search.html", result=result, text = text)

@app.route('/AboutUs')
def AboutUs():
    return render_template('AboutUs.html')


if __name__ == '__main__':
    app.run(threaded=False) #code needs to run on one thread for it to interact nicely with the database

    ##steps left visualise text data, implement map, geocode, visualise data on map, add sortin