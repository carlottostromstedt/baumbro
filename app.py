from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route("/")
def hello_baum():
    return "<p>Hello, Baum!</p>"

@app.route("/extract")
def extract_location():
    return render_template("extract.html")