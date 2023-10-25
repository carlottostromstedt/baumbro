from flask import Flask, render_template, redirect, request, session, url_for


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Sie sollten einen sicheren Schlüssel verwenden

# Datenbank mit Benutzerinformationen (einfache Demo)
users_db = {
    'testuser': 'password123'
}

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

@app.route("/extract")
def extract_location():
    return render_template("extract.html")