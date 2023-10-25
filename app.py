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
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        users_db[new_username] = new_password
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users_db and users_db[username] == password:
        session['username'] = username
        return redirect(url_for('profil'))
    return redirect(url_for('index'))

@app.route('/profil')
def profil():
    if 'username' in session:
        return render_template('profil.html', username=session['username'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
