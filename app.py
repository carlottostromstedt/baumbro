from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from location_utilities import *
import json
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Sie sollten einen sicheren Schlüssel verwenden
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

if __name__ == '__main__':
    app.run(debug=True)

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Trees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude  = db.Column(db.Float, nullable=False)
    kategorie = db.Column(db.String(250), nullable=True)
    baumartlat = db.Column(db.String(250), nullable=True)
    baumgattunglat = db.Column(db.String(250), nullable=True)
    baumnamedeu = db.Column(db.String(250), nullable=True)
    baumnamelat = db.Column(db.String(250), nullable=True)
    baumnummer = db.Column(db.String(250), nullable=True)
    baumtyptext = db.Column(db.String(250), nullable=True)

# Datenbank mit Benutzerinformationen (einfache Demo)
users_db = {
    'testuser': 'password123'
}

db.init_app(app)

def fill_db():
    # Specify the full path if the file is in a different directory.
    file_path = 'opendata/trees-04-10-2023.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    for baum in data['features']:
        tree = Trees(longitude=baum['geometry']['coordinates'][0],
         latitude=baum['geometry']['coordinates'][1],
         kategorie=baum['properties']['kategorie'],
         baumartlat=baum['properties']['baumartlat'],
         baumgattunglat=baum['properties']['baumgattunglat'],
         baumnamedeu=baum['properties']['baumnamedeu'],
         baumnamelat=baum['properties']['baumnamelat'],
         baumnummer=baum['properties']['baumnummer'],
         baumtyptext=baum['properties']['baumtyptext'])

        db.session.add(tree)
        db.session.commit()

with app.app_context():
    db.create_all()

# with app.app_context():
#     fill_db()

@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('profil'))
    return render_template('login.html')

@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("new_username")
        password = request.form.get("new_password")
 
        if not username or not password:
            error = 'Benutzername und Passwort dürfen nicht leer sein.'
            return render_template("sign_up.html", error=error)

        existing_user = Users.query.filter_by(username=username).first()
 
        if existing_user:
            error = 'Dieser Benutzername ist bereits vergeben. Bitte wählen Sie einen anderen.'
            return render_template("sign_up.html", error=error)
       
        else:
            user = Users(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
        return redirect(url_for("login"))
   
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()
 
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            return render_template("extract.html")
        else:
            error= 'Benutzername und Passwort dürfen nicht leer sein.t ungültig'
            return render_template("login.html", error=error)
 
    return render_template("login.html", error=error)

@app.route('/profil')
def profil():
    if 'username' in session:
        return render_template('profil.html', username=session['username'])
    return redirect(url_for('index'))

@app.route("/extract", methods=['GET', 'POST'])
def extract_location():
    if request.method == "POST":
        longitude_decimal = 0
        latitude_decimal = 0

        if 'picture' in request.files:
            print("Picture")
        else:
            print("NO PICTURE")
        
        if "longitude" in request.form and request.form.get("longitude") != "":
            longitude_decimal = request.form.get("longitude")
            latitude_decimal = request.form.get("latitude")
        elif 'picture' in request.files:
            print("IM ELIF BLOCK")
            picture_file = request.files['picture']
            longitude_decimal, latitude_decimal = get_coordinates(picture_file)

        markers=[
        {
        "lat": 51.5074,
        "lon": -0.1278,
        "popup": "This is London, UK."
        }
        ]
        return redirect(url_for("query", longitude= longitude_decimal, latitude=latitude_decimal, markers = markers))
    else:
        return render_template("extract.html")

# @app.route('/query/<id>')
# def query(id):
#     query = Query.query.filter_by(id=id).first_or_404()
#     markers = request.args.get('markers')
#     longitude_dictionary = calculate_query_values(query.longitude, query.latitude, 200)

#     b = Trees.query.filter(text("ROUND(longitude, 1) = ROUND(:longitude, 1) AND ROUND(latitude, 1) = ROUND(:latitude, 1)")).params(longitude=query.longitude, latitude=query.latitude).first_or_404()
#     return render_template("query.html", query=query, baum=baum, markers=markers)

@app.route('/query')
def query():
    markers = request.args.get('markers')
    longitude = float(request.args.get('longitude'))
    latitude = float(request.args.get('latitude'))
    location_dictionary = calculate_query_values(longitude, latitude, 200)

    baeume = Trees.query.filter(
        Trees.latitude.between(location_dictionary['minLatitude'], location_dictionary['maxLatitude']),
        Trees.longitude.between(location_dictionary['minLongitude'], location_dictionary['maxLongitude'])
    ).all()

    return render_template("query.html", query=query, baeume=baeume, markers=markers)

@app.route('/baum/<baumnummer>')
def baum(baumnummer):
    tree = Trees.query.filter_by(baumnummer=baumnummer).first()
    return render_template("baum.html", baum=tree)
