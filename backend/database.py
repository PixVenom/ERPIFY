# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

# Use pymysql for everything
pymysql.install_as_MySQLdb()

# SQLAlchemy DB URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:MySQLM4Pro@localhost/ERP"

# SQLAlchemy engine/session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Simple pymysql connection for raw SQL usage
def get_connection():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="MySQLM4Pro",
            database="ERP",
            auth_plugin="mysql_native_password",
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None