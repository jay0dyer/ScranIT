from flask import Flask, render_template, request, send_from_directory
import os
from ScranSearch import ScranSearchEngine

print("loading back end...")
engine = ScranSearchEngine()
app = Flask(__name__)

# READ BACKEND USAGE .TXT !!

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/', methods=['POST', 'GET'])
def landing_page_search():
    text = request.args.get('text', '')
    result=engine.Search(text)

    return render_template("search.html", result=result, text = text)


@app.route('/search')
def search():
    text = request.args.get('text', '')
    sort = request.args.get('sortBy', '')
    print(f"Search Query: {text}")
    print(f"Sort Option: {sort}")
    result=engine.Search(text, sort)

    return render_template("search.html", result=result, text = text)

@app.route('/AboutUs')
def AboutUs():
    return render_template('AboutUs.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'Images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')




if __name__ == '__main__':
    app.run(threaded=False) #code needs to run on one thread for it to interact nicely with the database

    ##steps left visualise text data, implement map, geocode, visualise data on map, add sortin