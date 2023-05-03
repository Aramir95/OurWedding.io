import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()



config = {
    'user': os.getenv('db_user'),
    'password': os.getenv('db_password'),
    'host': os.getenv('cloud_sql_host'),
    'database': os.getenv('db_name'),
}

cnx = mysql.connector.connect(**config)
