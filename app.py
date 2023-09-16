# Import libraries
from flask import Flask, render_template, redirect, url_for,request
from sqlalchemy import create_engine , text

app = Flask(__name__, template_folder="templates")
host = "aws.connect.psdb.cloud"
user = "ygg2zbfdcntdfxr152o6"
password = "pscale_pw_JoAgDLiFNDTU8ZWL3wJcKTirWLbwDmLFjgngov9uNJW"
database = "data-users"
connection_db = f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"
connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }

engine = create_engine(connection_db,connect_args=connect_args)

with engine.connect() as connection:
    result = connection.execute(text("select * from users"))

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
    if request.method == 'POST':
        data = request.json
        username = data.username
        password = data.password
        email = data.email
        check_query = f"select count(*) from users where username = '{username}' or email = '{email}'"
        query = f"insert into users(username, email, password_hash) values ('{username}', '{email}', '{password}')"
        with engine.connect() as connection:
            result = connection.execute(text(check_query))
            if result.all()[0][0]>=1:
                msg = "The username is already exist!"
            else:
                result = connection.execute(text(query))
                if result:
                    msg = "Successfully sign up!"
                else:
                    msg = "Failed to sign up!"
    return redirect(url_for('login')), msg

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login_page.html')

if __name__ == '__main__':    
    app.run(debug=True)
#git add .
# git commit -m "msg"
# git push -u origin main
# 