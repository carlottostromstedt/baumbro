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

## Flask Login

