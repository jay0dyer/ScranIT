from flask import Flask
from ScranSreach import ScranSreachEngine

app = Flask(__name__)

# READ BACKEND USAGE .TXT !!

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
