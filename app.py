from flask import Flask, flash, session, render_template, request, g, redirect, url_for
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from helper import generateScreenshot, hashed
import sqlite3
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
import os
import requests
from classes import User
import json

DATABASE = 'database.db'
app = Flask(__name__)
app.config["FLASK_APP"] = "app.py"
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = os.environ['FLASK_SECRET_KEY']


@app.route('/login/<e>', methods=['GET'])
@app.route('/login', methods=['GET', 'POST'])
def login(e=None):
    if request.method == 'POST':
        login_details = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        row = get_user_via_key('email', login_details['email'], "user")
        if not row:
            return render_template('login.html', e="0"), 401
            # return render_template('check.html', message="An Account with this Email doesn't exists.")
        else:
            if not hashed(login_details['password'])==row['password']:
                return render_template('login.html', e="1"), 401
                # return render_template('check.html', message="Please check the provided passwords.")
            else:
                login_user(load_user(row['user_id']))
                return redirect(url_for('dashboard'))
    else:
        if current_user.is_authenticated:
            print(current_user.is_authenticated)
            # Das ist Käse wir sollten an der stelle einfach direct zu dem zueghörigen Account redirecten
            return redirect(url_for('dashboard'))
        else:
            e = request.args.get('e')
            if e == "r_success":
                return render_template('login.html', e="r_success")
            else:
                return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('check.html', message="You are now logged out.", redirect="home", cta="Home")

@login_manager.user_loader
def load_user(id):
    user = User("placeholder", id)
    return user

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
                return render_template('register.html', e="2"), 401
            else:
                if not (register_details['password1']==register_details['password2']):
                    return render_template('register.html', e="3"), 401
                else:
                    hash = hashed(register_details['password1'])
                    db.execute('INSERT INTO user (email, firstname, lastname, password) VALUES (?, ?, ?, ?)', (register_details['email'], register_details['firstname'], register_details['lastname'], hash))
                    con.commit()
                    return redirect(url_for('login', e="r_success"))
    else:
        return render_template('register.html')

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    u = current_user.id
    row = get_user_via_key('user_id', u, "projects", True)
    newRow = [{} for _ in range(len(row))]
    for i in range(0, len(row)):
        newRow[i]['project_id'] = row[i]['project_id']
        newRow[i]['name'] = row[i]['name']
        newRow[i]['url'] = row[i]['url']
        newRow[i]['last_changed'] = row[i]['last_changed']
        newRow[i]['path'] = 'assets/thumbnails/'+str(row[i]['project_id'])+'.png'
    return render_template('dashboard.html', projects=newRow)

@app.route("/dashboard/newproject", methods=['GET', 'POST'])
@login_required
def newProject():
    if request.method == 'GET':
        return render_template('create_project.html')
    else:
        project_name = request.form['project_name']
        url = request.form['url']

        with sqlite3.connect(DATABASE) as con:
            con.row_factory = sqlite3.Row
            db = con.cursor()
            db.execute('INSERT INTO projects (user_id, name, url) VALUES (?, ?, ?)', (current_user.id, project_name, url))
            db.execute('SELECT last_insert_rowid()')
            rid = db.fetchone()
            con.commit()
            screen = generateScreenshot(url, rid[0])
            print(screen)
            return redirect(url_for('editProject', id=rid[0]))

@app.route("/project=<id>", methods=['GET'])
@login_required
def editProject(id):
    if request.method == 'GET':
        row = get_user_via_key('project_id', id, 'projects')
        if not row:
            return redirect(url_for('dashboard'))
        if not str(row['user_id']) == current_user.id:
            return redirect(url_for('dashboard'))
        else:
            changes = get_user_via_key('project_id', id, 'changes', True)
            return render_template('edit_project.html', url=row['url'], project_id=row['project_id'], changes=changes)

@app.route("/savechanges", methods=['POST'])
@login_required
def saveChanges():
    if request.method == 'POST':
        data = request.get_json()
        with sqlite3.connect(DATABASE) as con:
            con.row_factory = sqlite3.Row
            db = con.cursor()
            db.execute('INSERT INTO changes (project_id, selector, change_value, comment) VALUES (?, ?, ?, ?)', (data['project_id'], data['selector'], data['change_value'], data['comment']))
            con.commit()
        return "OK"


@app.route("/proxy/<path:url>", methods=['GET'])
@login_required
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

def get_user_via_key(database_key, key_value, table_name, multiple=False):
    with sqlite3.connect(DATABASE) as con:
        con.row_factory = sqlite3.Row
        db = con.cursor()
        len = db.execute('SELECT * FROM ' +table_name +' WHERE ' + database_key + '=?', [(key_value)])
        if not multiple:
            db_row = db.fetchone()
            return db_row
        else:
            ret = []
            for row in len:
                ret.append(row)
            return ret

###can't get them out of this file lol
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
