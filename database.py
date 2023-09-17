from sqlalchemy import create_engine , text
import os
# host = "localhost"
# user = "root"
# password = "pscale_pw_vc0Uq1jSdgv4UIJ9DSIND0g9iKBdPWL3xVp65NVek6A"

# database = "users"
# connection_db = f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"
# connect_args={
#         "ssl": {
#             "ssl_ca": "/etc/ssl/cert.pem"
#         }
#     }
connection_db = "mysql+pymysql://9ywrth98njylsobn3prl:pscale_pw_MRwxhQ0v87I0NUd1laJYk9RXUJIvrIaOnTYfI86mOZI@aws.connect.psdb.cloud/data-users?charset=utf8mb4"
connect_args = {"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}}
engine = create_engine(connection_db, connect_args=connect_args)

def load_data():
    with engine.connect() as conn:
        query = "SELECT id, username, email, password_hash FROM users"
        result = conn.execute(text(query))
        data = result.all()
        
        results = [{
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'password': row[3]
        } for row in data]
        
        return results

    
def check_if_exist(username, email):
    email_exist = False
    username_exist = False
    QUERY = f"SELECT * FROM users WHERE username='{username}' OR email='{email}'"
    with engine.connect() as conn:
        result = conn.execute(text(QUERY)).all()
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
        result = conn.execute(QUERY, parameters=parameters)
        
    return result

print(login_function("wissal"))
# check_if_exist("wissal","wissal@gmail.com")