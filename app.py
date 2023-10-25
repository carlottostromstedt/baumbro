import trees;
from flask import Flask, render_template, request, url_for, redirect
from flask_login import current_user

app = Flask(__name__)

@app.route("/")
def hello_baum():
    return "<p>Hello, Baum!</p>"

@app.route('/upload_coordinates', methods=['POST'])
def upload_coordinates():
    if request.method == "POST":
        user_lat = request.form.get('user_lat')
        user_lon = request.form.get('user_lon')
        requestObject = trees.Request(user_lat, user_lon, current_user.username)
        db.session.add(requestObject)
        db.session.commit
    return render_template("upload_pic.html")

#    execute_tree_search()

@app.route("/extract")
def extract_location():
    return render_template("extract.html")


#   in arbeit
@app.route('/upload', methods=['POST'])
def upload_image():
    trees.execute_tree_search()

    uploaded_image = request.files['image']
    if uploaded_image:
        image_data = uploaded_image.read()
        
        image = Image.open(io.BytesIO(image_data))
        
        exif_data = image._getexif()
        
        if exif_data:
            exif_data = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
            if 'GPSInfo' in exif_data:
                gps_info = {GPSTAGS.get(gps_tag, gps_tag): gps_value for gps_tag, gps_value in exif_data['GPSInfo'].items()}
                latitude = gps_info.get('GPSLatitude')
                longitude = gps_info.get('GPSLongitude')
                return f"Latitude: {latitude}, Longitude: {longitude}"
    
    return "Keine GPS-Daten gefunden."

