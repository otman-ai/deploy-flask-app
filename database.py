from sqlalchemy import create_engine , text

host = "aws.connect.psdb.cloud"
user = "57nh0lnmkrho72pru6qe"
password = "pscale_pw_to6kijCRtKPCXbkHxLDDTlxOHASG6YBVR6pzKo0T9Pt"
database = "data-users"
connection_db = f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"
connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
engine = create_engine(connection_db,connect_args=connect_args)