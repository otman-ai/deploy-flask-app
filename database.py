from sqlalchemy import create_engine , text
import os

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
username = "wissal_waaziz123"
email = "wissal_waaziz123@gmail.com"
pas = "wissal_waaziz123A1"
query = f"insert into users(username, email, password_hash) values ('{username}', '{email}', '{pas}')"
print(query)
with engine.connect() as connection:
    result = connection.execute(text(query))
    if result:
        print("YES")
    else:
        print("NO")
