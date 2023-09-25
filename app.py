# Import libraries
from flask import Flask,render_template, redirect, url_for, request, jsonify, session, Response
from database import *
from werkzeug.security import generate_password_hash, check_password_hash
import os 
from constant import *
import datetime
import requests

import boto3
import uuid
import dotenv
from werkzeug.datastructures import Headers

dotenv.load_dotenv()
app = Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(24)
video_keys = []
S3_BUCKET_NAME = 'usersuploadedvideos'
s3 =  boto3.client(
    service_name='s3',
    region_name='eu-north-1',
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)

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


@app.route('/check_ips', methods=['GET'])
def check_ips():
    ip_adresses = []
    ids = []
    if 'username' in session:
        data = load_data(session["username"]) 
        for camera in data:
            camera_ip_address = camera['camera_ipAdress']
            ids.append(str(camera['id']))
            ip_adresses.append(camera_ip_address)
    
    return jsonify({"ip_adresses":ip_adresses,"ids":ids})

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

@app.route('/video/<path:key>')
def serve_video(key):
    # Replace 'https://example.com/video.mp4' with the actual video URL
    remote_url = f'https://d2j0jiqttqesr8.cloudfront.net/{key}'
    # Send a request to the remote URL and stream the video content
    response = requests.get(remote_url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Set the content type and headers for the video
        headers = {
            'Content-Type': 'video/mp4',
            'Content-Disposition': 'inline; filename="video.mp4"'
        }

        # Stream the video content to the Flask response
        return Response(response.iter_content(chunk_size=1024), headers=headers, content_type='video/mp4')

@app.route('/dash', methods=["GET", "POST"])
def dash():
    is_videoExist = False
    if 'username' in session:
        img_data = None
        video_url = ''
        if request.method == 'POST':
            if 'video' in request.files:
                video = request.files["video"]


                # Upload to Amazon S3 (requires proper AWS setup)
                key = 'upload/'+ str(uuid.uuid4())+".mp4"
                s3.upload_fileobj(video, S3_BUCKET_NAME, key)
                # s3.upload_file(temp_video_file.name, S3_BUCKET_NAME, key)
                # Send the POST request with JSON data to the external service
                url = 'http://ec2-13-48-135-42.eu-north-1.compute.amazonaws.com/predict'
                data_key = {'Key': key}
                print("data_key",data_key)
                user = login_function(session["username"])[0]
                data = load_data(session["username"])
                response = requests.post(url, json=data_key)
                if 'Key' in response.json():
                    video_key = response.json()['Key']
                    video_keys.append(video_key)
                    is_videoExist = True
                    video_url = f'/video/{video_key}'
                    print(response.json())
                    return render_template("dashboard_templates/dash.html", 
                                           user=user,cameras=data,video_url=video_url)
                else:
                    print(response.json())
            else:  
                data = request.get_json()
                ipAddress = data.get('ipAddress')
                port = data.get('port')
                camera_ipAdress = f"http://{ipAddress}:{port}/video"               
                current_datetime = datetime.datetime.now()                    
                formatted_datetime = current_datetime.strftime("%Y-%b-%d:%H:%M:%S")[:-3]
                camera_date = formatted_datetime

                user_id = get_user_id(session['username'])
                camera_id = insert_to_camera(user_id, camera_ipAdress, camera_date)
                if camera_id:
                    output_dir = UPLOAD_FOLDER+f"{user_id}/{camera_id}/"
                    camera_name = f"Camera  {camera_id}"
                    db_update = insert_to_camera_part(camera_name, output_dir)
                else:
                    print("Error while inserting to db.")

        user = login_function(session["username"])[0]
        data = load_data(session["username"])
        return render_template("dashboard_templates/dash.html", user=user,cameras=data, is_video = is_videoExist)
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
    if "username" in session:
        data = load_data(session["username"]) 
        print(data)
        return jsonify(data)
    return redirect(url_for("login"))

if __name__ == '__main__':    
    app.run(host='0.0.0.0',debug=True)
#git add .
# git commit -m "msg"
# git push -u origin main
# 