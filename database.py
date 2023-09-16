from sqlalchemy import create_engine , text

host = "aws.connect.psdb.cloud"
user = "bq73ovk7a2gw1w0i0rez"
password = "pscale_pw_TVGY7045qaH2Lp3r9lHd59wvbqM1bBVr85ZnBsbyYKy"
database = "data-users"
connection_db = f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"
connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
engine = create_engine(connection_db,connect_args=connect_args)
def load_data():
    with engine.connect() as conn:
        query = "select * from users"
        result = conn.execute(text(query))
        data = result.all()
        results = [
        {
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'password': row[3]
        }
        for row in data
    ]
        return results