from sqlalchemy import create_engine , text

host = "aws.connect.psdb.cloud"
user = "0b6lfqrst79nbtyy4y3l"
password = "pscale_pw_vc0Uq1jSdgv4UIJ9DSIND0g9iKBdPWL3xVp65NVek6A"
database = "data-users"
connection_db = f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"
connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
engine = create_engine(connection_db,connect_args=connect_args)