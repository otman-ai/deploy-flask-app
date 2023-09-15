# Import libraries
from flask import Flask, render_template, redirect, url_for
app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return redirect(url_for('login'))
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404_page.html"), 404
@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login_page.html')

if __name__ == '__main__':    
    app.run(debug=True)
