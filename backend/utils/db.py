import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="pixvenom",
            password="MySQLM4Pro",
            database="ERP"
        )
        return connection
    except Error as e:
        print("Database connection failed:", e)
        return None
