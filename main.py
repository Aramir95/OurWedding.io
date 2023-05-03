from Class.CrearDataBaseSQL import DataBaseMySQL
import os
from dotenv import load_dotenv

load_dotenv()

guest_excel=os.path.join(os.path.dirname(os.path.abspath(__file__)),"Data","guest.xlsx")

config = {
    'user': os.getenv('db_user'),
    'password': os.getenv('db_password'),
    'host': os.getenv('cloud_sql_host'),
    'database': os.getenv('db_name'),
    'port': os.getenv('db_port'),
}

db = DataBaseMySQL(host=config['host'], user=config['user'], password=config['password'], database_name=config['database'], port=config['port'])
db.import_table_from_excel(name_table="Lista_invitados",path_excel=guest_excel)
db.close()