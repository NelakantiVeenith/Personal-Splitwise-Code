# database.py
import mysql.connector

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            user="root",
            password="Veenithn143@",
            host="localhost",
            database="my_sql"  # You can change this to your preferred database
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def connect_to_database2(head):
    try:
        conn = mysql.connector.connect(
            user="root",
            password="Veenithn143@",
            host="localhost",
            database=head  # You can change this to your preferred database
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

