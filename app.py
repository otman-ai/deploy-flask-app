# Import libraries
from flask import Flask, render_template, redirect, url_for,request,jsonify, session
from sqlalchemy import create_engine , text
from database import *
from werkzeug.security import generate_password_hash, check_password_hash

import os 

app = Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(24)
@app.route('/check', methods=['POST'])
def check():
    data = request.json
    username = data['username']
    email = data['email']
    user_by_username, user_by_email = check_if_exist(username, email)

    result = {
        'usernameExists': user_by_username ,
        'emailExists': user_by_email ,
    }
    return jsonify(result)


@app.route("/")
def home():
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404_page.html"), 404

@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/access_denied")
def access_denied():
    return render_template("access_denied.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username-sign-up']
        password = request.form['password-sign-up']
        email = request.form['email']
        hashed_password = generate_password_hash(password)
        ok_ = insert_to_db(username, hashed_password, email)
        if ok_:
            return redirect(url_for("login"))
    return render_template('login_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(url_for("dash"))
    if request.method == 'POST':
        username = request.form['username-sign-in']
        password = request.form['password-sign-in']

        user = login_function(username)
        if user != [] and  check_password_hash(user[0][3], password):
            session['username'] = username
            return redirect(url_for("dash"))
        return render_template('login_page.html',message1="The username or password you entered is incorrect")
    return render_template('login_page.html')


@app.route('/dash', methods=["GET", "POST"])
def dash():
    if 'username' in session:
        user = login_function(session["username"])[0]
        return render_template("dashboard_templates/dash.html", user=user)
    return redirect(url_for("login"))

@app.route('/dash/cameras', methods=["GET", "POST"])
def cameras():
    if 'username' in session:
        user = login_function(session["username"])[0]
        if user:
            return render_template("dashboard_templates/cameras.html", user=user)
        else:
            return render_template("access_denied.html")
    else:
        return redirect(url_for('login'))


@app.route('/dash/security', methods=["GET", "POST"])
def security():
    if 'username' in session:
        user = login_function(session["username"])[0]
        if user:
            return render_template("dashboard_templates/security.html", user=user)
        else:
            return render_template("access_denied.html")
    else:
        return redirect(url_for('login'))

@app.route('/dash/storage', methods=["GET", "POST"])
def storage():
    if 'username' in session:
        user = login_function(session["username"])[0]
        if user:
            return render_template("dashboard_templates/storage.html", user=user)
        else:
            return render_template("access_denied.html")
    else:
        return redirect(url_for('login'))


@app.route('/dash/users', methods=["GET", "POST"])
def users():
    if 'username' in session:
        user = login_function(session["username"])[0]
        if user:
            return render_template("dashboard_templates/users.html", user=user)
        else:
            return render_template("access_denied.html")
    else:
        return redirect(url_for('login'))

@app.route('/dash/reports', methods=["GET", "POST"])
def reports():
    if 'username' in session:
        user = login_function(session["username"])[0]
        if user:
            return render_template("dashboard_templates/reports.html", user=user)
        else:
            return render_template("access_denied.html")
    else:
        return redirect(url_for('login'))
    

@app.route('/dash/support', methods=["GET", "POST"])
def support():
    if 'username' in session:
        user = login_function(session["username"])[0]
        if user:
            return render_template("dashboard_templates/support.html", user=user)
        else:
            return render_template("access_denied.html")
    else:
        return redirect(url_for('login'))
    
@app.route('/dash/settings', methods=["GET", "POST"])
def settings():
    if 'username' in session:
        user = login_function(session["username"])[0]
        if user:
            return render_template("dashboard_templates/settings.html", user=user)
        else:
            return render_template("access_denied.html")
    else:
        return redirect(url_for('login'))

@app.route('/dash/account', methods=["GET", "POST"])
def account():
    if 'username' in session:
        user = login_function(session["username"])[0]
        if user:
            return render_template("dashboard_templates/account.html", user=user)
        else:
            return render_template("access_denied.html")
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/api')
def api():
    data = load_data() 
    return jsonify(data)

if __name__ == '__main__':    
    app.run(host='0.0.0.0',debug=True)
#git add .
# git commit -m "msg"
# git push -u origin main
# 