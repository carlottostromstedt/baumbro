from flask import Flask
from db.db import init_db

app = Flask(__name__)

init_db(app)

@app.route("/")
def hello_baum():
    return "<p>Hello, Baum!</p>"
