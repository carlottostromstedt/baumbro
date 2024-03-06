from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Sie sollten einen sicheren Schlüssel verwenden
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db = SQLAlchemy()

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude  = db.Column(db.Float, nullable=False)

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

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('profil'))
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
 
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
            return redirect(url_for("home"))
        else:
            error= 'Benutzername oder Passwort ist ungültig'
 
    return render_template("login.html", error=error)

@app.route('/profil')
def profil():
    if 'username' in session:
        return render_template('profil.html', username=session['username'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

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

        query = Query(longitude = longitude_decimal, latitude = latitude_decimal)
        db.session.add(query)
        db.session.commit()

        markers=[
        {
        "lat": 51.5074,
        "lon": -0.1278,
        "popup": "This is London, UK."
        }
        ]
        return redirect(url_for("query", id=query.id, query=query, longitude= longitude_decimal, latitude=latitude_decimal, markers = markers))
    else:
        return render_template("extract.html")

@app.route('/query/<id>')
def query(id):
    query = Query.query.filter_by(id=id).first_or_404()
    markers = request.args.get('markers')
    baum = Trees.query.filter(text("ROUND(longitude, 1) = ROUND(:longitude, 1) AND ROUND(latitude, 1) = ROUND(:latitude, 1)")).params(longitude=query.longitude, latitude=query.latitude).first_or_404()
    return render_template("query.html", query=query, baum=baum, markers=markers)

def get_exif_data(image):
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_data[decoded] = value
            if decoded == "GPSInfo":
                gps_info = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = value[t]
                exif_data[decoded] = gps_info
    return exif_data

def get_gps_info(image_path):
    with Image.open(image_path) as img:
        exif_data = get_exif_data(img)
        if "GPSInfo" in exif_data:
            gps_info = exif_data["GPSInfo"]
            if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                latitude = gps_info["GPSLatitude"]
                longitude = gps_info["GPSLongitude"]
                return latitude, longitude
    return None, None

def convert_to_decimal_degrees(coord):
    degrees, minutes, seconds = coord
    decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
    return decimal_degrees

def get_coordinates(picture_file):
        img = Image.open(picture_file)
        img_exif = img.getexif()
        print(img_exif)
        print(get_gps_info(picture_file))
        latitude, longitude = get_gps_info(picture_file)
        latitude_decimal = convert_to_decimal_degrees(latitude)
        longitude_decimal = convert_to_decimal_degrees(longitude)

        print("Latitude (Decimal Degrees):", latitude_decimal)
        print("Longitude (Decimal Degrees):", longitude_decimal)
        # <class 'PIL.Image.Exif'>
        if img_exif is None:
            print('Sorry, image has no exif data.')
        else:
            for key, val in img_exif.items():
                if key in ExifTags.TAGS:
                    print(f'{ExifTags.TAGS[key]}:{val}')
                else:
                    print(f'{key}:{val}')
        return longitude_decimal, latitude_decimal