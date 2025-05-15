from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

# Ensure pymysql is used as MySQLdb (only needed if using libraries expecting MySQLdb)
pymysql.install_as_MySQLdb()

# SQLAlchemy connection URL (using pymysql)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:MySQLM4Pro@localhost/ERP"

# SQLAlchemy engine and session setup
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Optional but helps with connection handling
)

# SessionLocal for creating session instances to interact with DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Raw pymysql connection function (for cursor-based DB access)
def get_connection():
    try:
        # Return pymysql connection with dictionary cursor
        return pymysql.connect(
            host="localhost",
            user="root",  # Your MySQL username
            password="MySQLM4Pro",  # Your MySQL password
            database="ERP",  # Your MySQL database name
            cursorclass=pymysql.cursors.DictCursor # This will ensure rows are returned as dictionaries
        )
    except Exception as e:
        print("Database connection failed:", str(e))
        return None

# Optional: You can include a function for closing the session/connection cleanly
def close_session(session):
    try:
        session.close()
    except Exception as e:
        print("Failed to close session:", str(e))
