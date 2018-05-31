from flask import Flask, render_template, request
from urllib.parse import urlsplit
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
        url = request.form.get('url')
        print(url)
        return render_template('edit_post.html', url=url)

@app.route("/proxy/<path:url>", methods=['GET'])
def proxy(url):
    print(request.args.get('url'))
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    newtag_base = soup.new_tag('base')
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    newtag_base.attrs['href'] = base_url
    soup.head.insert(0, newtag_base)

    newtag_link = soup.new_tag('link')
    newtag_link.attrs['rel'] = "stylesheet"
    newtag_link.attrs['type'] = "text/css"
    newtag_link.attrs['href'] = "/static/style.css"
    soup.head.insert(0, newtag_link)

    return soup.renderContents()
