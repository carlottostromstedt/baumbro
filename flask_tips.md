# Tips for Flask

to launch your environment:

insert your environment name for `<env-name>`

Linux / Mac:
```bash
source <env-name>/bin/activate
```

Windows:

```bash
<env-name>/Scripts/activate
```

## Base HTML

You can create a base HTML which contains Navbar and everything and then just insert the other HTMLs inside of that base html. This way you always have a navbar on every page and you dont have to define the whole HTML structure every time you add a template.

```HTML
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
	<title>Forbidden Memories - Fusion Friend</title>
</head>
<body>
	<nav class="navbar">
	<div class="container">
	<a class="navbar-brand" href="/">FM</a>
	<ul class="nav-list">
		{% if current_user.is_authenticated %}
		<li><a href="/">Home</a></li>
		<li><a href="/logout">Logout</a></li>
		<li><a href="/boards">Boards</a></li>
		<li><a href="/upload">Upload</a></li>
		{% else %}
		<li><a href="/">Home</a></li>
		<li><a href="/login">Login</a></li>
		<li><a href="/register">Register</a></li>
		{% endif %}
		</ul>
	</div>
	</nav>
	{% block content %}
	{% endblock %}
</body>

</html>

```

### Jinja2

Flask uses jinja Syntax to allow you to use loops, add variables and other constructs inside of your html.

Inside of your base HTML  body you should have this:

```HTML
<body>
	{% block content %}
	{% endblock %}
</body>
```

Then inside of your template HTMLs you use this

```HTML
{% extends "base.html" %}

{% block content %}
  <h1>Hello</h1>
{% endblock %}
```

The HTML inside of the block is combined with your base.html during page load

So the whole page (generated) would look like this:

```HTML
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
	<title>Forbidden Memories - Fusion Friend</title>
</head>
<body>
	<nav class="navbar">
	<div class="container">
	<a class="navbar-brand" href="/">FM</a>
	<ul class="nav-list">
		{% if current_user.is_authenticated %}
		<li><a href="/">Home</a></li>
		<li><a href="/logout">Logout</a></li>
		<li><a href="/boards">Boards</a></li>
		<li><a href="/upload">Upload</a></li>
		{% else %}
		<li><a href="/">Home</a></li>
		<li><a href="/login">Login</a></li>
		<li><a href="/register">Register</a></li>
		{% endif %}
		</ul>
	</div>
	</nav>
	## This is inserted
	<h1>Hello<h1>
</body>
</html>
```



## SqlAlchemy

use this to create a link to your DB. You can also use this to directly create models tied to the DB

Use this to install flask sqlalchemy (inside of terminal):

```bash
pip install flask-sqlalchemy
```

then import it at the top of your main/app.py file:

```python
from flask_sqlalchemy import SQLAlchemy
```

Config your database URL. Here with SQLite DB. After the import line:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
```

### Create db

To actually create the db do this after the app.config line

```python
db = SQLAlchemy()
```

### Create a class / model

Create a class (here Board) using this syntax:

```python
class Board(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(250), unique=True, nullable=False)
	filename = db.Column(db.String(250), unique=True, nullable=False)
```

### Initialize db

this initializes the db and creates the tables that you defined 

```python
db.init_app(app)

with app.app_context():
	db.create_all()
```

the variable `app` is the variable that we define at the top of our flask main/app file

```python
app = Flask(__name__)
```

### Saving to DB

To save to db we can create an Object of a defined Class with the required fields.

We can add the object with `db.session.add(object)`

And commit it with `db.session.commit`

```python
@app.route('/create', methods=["GET", "POST"])
	def create():
	if request.method == "POST":
	board = Board(name=request.form.get("name"))
	db.session.add(board)
	db.session.commit()
	return redirect(url_for("BOARD"))
	return render_template("create_board.html")
```



## Define a Route:

This is how you define a route:

```python
@app.route("/")
	def home():
	return render_template("home.html")
```

the `"/"` is the actual path that you will use in the URL.

with `def home()` you define the function that will be executed when you visit the route

Normally you would `return render_template()` at the end of the function. This just ensures that we display the page / template we want to.

A template is a html file inside of the `template` folder inside of the route directory.

To use `render_template()` we have to import it at the top of the main/app.py file:

```python
from flask import Flask, render_template
```

### Redirect

Can be used inside of a function to redirect to a page. Can be useful for example if you have a form and want the user to be redirected back to an index page once he has submitted the form.

```python
from flask import Flask, redirect

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))
```

Here the User is redirected to home after logging out.

## Forms

### Get data from form and save it

### HTML

```html
{% extends "base.html" %}

{% block content %}
<h1>Create a Board</h1>
	<form action="#" method="post">
	<label for="name">Name:</label>
	<input type="text" name="name" />
	<button type="submit">Submit</button>
</form>
{% endblock %}
```

### app.py / main.py - process the input data

Use `request.form.get("name-of-input-form")` to get the data from the form and put it inside of an Object. 

```python
@app.route('/create', methods=["GET", "POST"])
	def create():
	if request.method == "POST":
	board = Board(name=request.form.get("name"))
	db.session.add(board)
	db.session.commit()
	return redirect(url_for("BOARD"))
	return render_template("create_board.html")
```

## Flask Login

```bash
pip install flask-login
```

Follow this guide: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

## File upload

### Upload Folder

Define an upload folder as an environment variable and define which file extensions are allowed.

```python
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
```

Define a function to check if filename (file extension) is allowed

```python
def allowed_file(filename):
	return '.' in filename and \
	filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### HTML Form

Create a form with a file input

```HTML
{% extends "base.html" %}

{% block content %}
<title>Upload new File</title>
<h1>Upload new File</h1>
<form method=post enctype=multipart/form-data>
	<input type=file name=file>
	<input type=submit value=Upload>
</form>
{% endblock %}
```

### Route

Define a route and process the input from the Form. Here i also assign the filename to a Board object so i can access the file later with the filename.

```python
@app.route('/upload', methods=['GET', 'POST'])
	def upload_file():
		if request.method == 'POST':
		# Check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
		return redirect(request.url)
		file = request.files['file']
		# If the user does not select a file, the browser also
		# submits an empty part without a filename
		if file.filename == '':
		flash('No selected file')
		return redirect(request.url)
		if file and allowed_file(file.filename):
		# Generate a unique filename
		unique_filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
		# Create a new board with filename
		board = Board(name=boardname, filename=unique_filename)
		db.session.add(board)
		db.session.commit()
		return redirect(url_for('home'))
	
	return render_template("upload.html")
```

