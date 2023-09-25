from sqlalchemy import create_engine , text
import os
connection_db = os.environ['DB_CONNECTION_STRING']

connect_args = {"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}}
engine = create_engine(connection_db, connect_args=connect_args)


def load_data_condition(id):
    with engine.connect() as conn:
        query = "SELECT * FROM cameras where id= :id"
        result = conn.execute(text(query), parameters={"id":id})
        data = result.all()
        if data != []:
            return data[0][2]

def load_data(username):
    user_id = get_user_id(username)
    with engine.connect() as conn:
        query = "SELECT * FROM cameras where user_id= :user_id"
        result = conn.execute(text(query), parameters={"user_id":user_id})
        data = result.all()
        dict_data = [{
            "id":row[0],
            "camera_ipAdress":row[2],
            "camera_date":row[3],
            "camera_name":row[4],
            "video_saved_path":row[5]
        } for row in data]

        return dict_data


def get_user_id(username):
    with engine.connect() as conn:
        query = "SELECT * FROM users where username= :username"
        result = conn.execute(text(query), parameters={"username":username})
        data = result.all()
        if len(data) >=1:
            return data[0][0]

def check_if_exist(username, email):
    email_exist = False
    username_exist = False
    QUERY = f"SELECT * FROM users WHERE username= :username OR email= :email"
    with engine.connect() as conn:
        result = conn.execute(text(QUERY),parameters={"username":username, "email":email}).all()
        for i in result:
            if i[2] == email:
                email_exist = True
            if i[1] == username:
                username_exist = True
        return username_exist, email_exist
def insert_to_db(username, password, email):
    QUERY = text("INSERT INTO users (username, email, password_hash) VALUES (:username, :email, :password)")
    with engine.connect() as conn:
        result = conn.execute(QUERY, {"username": username, "email": email, "password": password})
        conn.commit()
        if result.rowcount > 0:
            return True
        return False
    
def login_function(username):    
    QUERY = text("SELECT * FROM users WHERE username = :username")
    
    with engine.connect() as conn:
        parameters = dict(username=username)
        result = conn.execute(QUERY, parameters=parameters).all()
        
    return result


def insert_to_camera(user_id,camera_ipAdress,camera_date):
    parametres = {"user_id":user_id, "camera_ipAdress":camera_ipAdress, "camera_date":camera_date}
    QUERY = text("INSERT INTO cameras  (user_id, camera_ipAdress, camera_date ) VALUES (:user_id, :camera_ipAdress, :camera_date)")
    with engine.connect() as conn:
        result = conn.execute(QUERY,parameters=parametres)
        conn.commit()
        if result.rowcount > 0:
            result_2 = conn.execute(text("SELECT * FROM cameras where camera_ipAdress=:camera_ipAdress"),
                                    parameters={"camera_ipAdress":camera_ipAdress}).all()
            id = result_2[0][0]
            return id
        return False
    
def insert_to_camera_part(camera_name ,video_saved_path ):
    QUERY = text("UPDATE cameras SET camera_name=:camera_name, video_saved_path =:video_saved_path WHERE id= LAST_INSERT_ID();")
    with engine.connect() as conn:
        result = conn.execute(QUERY,parameters={'camera_name':camera_name, 'video_saved_path':video_saved_path})
        conn.commit()
        if result.rowcount > 0:
            return True
        return False

