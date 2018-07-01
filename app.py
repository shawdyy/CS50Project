from flask import Flask, flash, session, render_template, request, g, redirect, url_for
from flask_login import LoginManager, login_required
import sqlite3
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
import os
import requests

DATABASE = 'database.db'
app = Flask(__name__)
app.config["FLASK_APP"] = "app.py"
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = os.environ['FLASK_SECRET_KEY']

###
# Der Spaß läuft hier noch nicht. session[key] ist anscheinend kein geeigneter check, ob jemand eingeloggt ist.
# Wir müssen einen richtigen check für eingeloggte user an die routes setzen um richtige redirects zu setzen

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_details = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        with sqlite3.connect(DATABASE) as con:
            con.row_factory = sqlite3.Row
            db = con.cursor()
            db.execute('SELECT user_id, password, firstname FROM user WHERE email=?', [(login_details['email'])])
            db_row = db.fetchone()
            if not db_row:
                return render_template('check.html', message="An Account with this Email doesn't exists.")
            else:
                if not login_details['password']==db_row['password']:
                    return render_template('check.html', message="Please check the provided passwords.")
                else:
                    session['username'] = request.form['email']
                    return render_template('check.html', message="Welcome back " + db_row['firstname'])
    else:
        if session['username']:
            return render_template('check.html', message="Yo are already logged in!")
        else:
            return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_details = {
            'firstname': request.form['first_name'],
            'lastname': request.form['last_name'],
            'email': request.form['email'],
            'password1': request.form['password'],
            'password2': request.form['password2']
        }

        with sqlite3.connect(DATABASE) as con:
            con.row_factory = sqlite3.Row
            db = con.cursor()
            db.execute('SELECT user_id FROM user WHERE email=?', [(register_details['email'])])
            db_row = db.fetchone()
            if db_row:
                return render_template('check.html', message="An Account with this Email already exists.")
            else:
                if not register_details['password1']==register_details['password2']:
                    return render_template('check.html', message="Please check the provided passwords.")
                else:
                    db.execute('INSERT INTO user (email, firstname, lastname, password) VALUES (?, ?, ?, ?)', (register_details['email'], register_details['firstname'], register_details['lastname'], register_details['password1']))
                    con.commit()
                    return render_template('check.html', message="Welcome "+ register_details['firstname'] + "! Login to use wype.io.")
    else:
        return render_template('register.html')

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/createproject", methods=['GET'])
@login_required
def edit():
    if request.method == 'GET':
        if session['username']:
            return render_template('create_project.html')
        else:
            return redirect(url_for('login'))

@app.route("/search", methods=['GET'])
def searchURL():
    if request.method == 'GET':
        url = unquote(request.args.get('url'))
        print(url)
        return render_template('edit_project.html', url=url)

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

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))
