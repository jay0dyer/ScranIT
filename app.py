from flask import Flask, render_template, request
from ScranSearch import ScranSearchEngine
import json
engine = ScranSearchEngine()
app = Flask(__name__)

# READ BACKEND USAGE .TXT !!

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html') # this links us to the templates

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    print(text)
    result=engine.Search(text)

    return render_template("index.html", result=result, text = text)





if __name__ == '__main__':
    app.run(threaded=False) #code needs to run on one thread for it to interact nicely with the database

    ##steps left visualise text data, implement map, geocode, visualise data on map, add sortin