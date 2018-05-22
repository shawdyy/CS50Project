from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import os
import requests

os.environ["FLASK_APP"] = "app.py"
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        return render_template('edit_get.html')
    else:
        return render_template('edit_post.html')

@app.route("/proxy", methods=['GET'])
def proxy():
    url = 'https://www.3mdeutschland.de/3M/de_DE/unternehmen-de/'
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c)
    newtag = soup.new_tag('base')
    newtag.attrs['href'] = "https://www.3mdeutschland.de"
    soup.head.insert(0, newtag)
    return soup.renderContents()
