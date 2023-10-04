import trees;
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_baum():
    return "<p>Hello, Baum!</p>"


@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    user_lat = 0; # irgendwie Breitengrad holen 
    user_lon = 0;# irgendwie Breitengrad holen

    # Verwende die importierte Methode
    nearest_tree = find_nearest_tree(float(user_lat), float(user_lon))

    return f"Der nächste dokumentierte Baum ist: {nearest_tree['tree_name']} in einer Entfernung von {nearest_tree['distance']} km."
