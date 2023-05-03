from Class.CrearDataBaseSQL import DataBaseMySQL
from Class.DataGuests import DataGuests
import os
from dotenv import load_dotenv

load_dotenv()

guest_excel=os.path.join(os.path.dirname(os.path.abspath(__file__)),"Data","guest.xlsx")

#Cargar y actualizar archivo de invitados
data=DataGuests()._frame

config = {
    'user': os.getenv('db_user'),
    'password': os.getenv('db_password'),
    'host': os.getenv('cloud_sql_host'),
    'database': os.getenv('db_name'),
    'port': os.getenv('db_port'),
}

db = DataBaseMySQL(host=config['host'], user=config['user'], password=config['password'], database_name=config['database'], port=config['port'])
db.from_dataframe_create_table(name_table="Lista_de_invitados",df=data)
db.close()