from flask import Flask, render_template, request, g
import sqlite3
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
import os
import requests

DATABASE = 'database.db'
os.environ["FLASK_APP"] = "app.py"
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/", methods=['GET'])
def edit():
    if request.method == 'GET':
        return render_template('edit_get.html')

@app.route("/search", methods=['GET'])
def searchURL():
    if request.method == 'GET':
        url = unquote(request.args.get('url'))
        print(url)
        return render_template('edit_post.html', url=url)

@app.route("/savechanges", methods=['POST'])
def saveChanges():
    if request.method == 'POST':
        data = request.get_json()
        print(data)

@app.route("/proxy/<path:url>", methods=['GET'])
def proxy(url):
    if not 'http://' in url and not 'https://' in url:
        useable_url = 'http://' + url
    else:
        useable_url = url
    print(useable_url)
    try:
        r = requests.get(useable_url)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")

        newtag_base = soup.new_tag('base')
        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(r.url))
        newtag_base.attrs['href'] = base_url
        soup.head.insert(0, newtag_base)

        newtag_link = soup.new_tag('link')
        newtag_link.attrs['rel'] = "stylesheet"
        newtag_link.attrs['type'] = "text/css"
        newtag_link.attrs['href'] = "/static/style.css"
        soup.head.insert(0, newtag_link)

        return soup.renderContents()
    except:
        return "Please provide a valid url"
