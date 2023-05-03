import pymysql
import logging
import pandas as pd
import json


class FailConect(Exception):
    """Excepción que se lanza cuando no se puede establecer una conexión con la base de datos."""
    def __init__(self, message):
        """Inicializa la excepción con un mensaje de error."""
        self.message = message
    
    def __str__(self):
        return self.message

class DataBaseMySQL:
    """Clase que representa una base de datos MySQL.

    Atributos:
        host (str): El host de la base de datos.
        port (int): El puerto de la base de datos.
        user (str): El nombre de usuario para conectarse a la base de datos.
        password (str): La contraseña para conectarse a la base de datos.
        database_name (str): El nombre de la base de datos.
        conn (pymysql.connections.Connection): La conexión a la base de datos.
    """

    def __init__(self , host: str, port: str , user: str, password: str, database_name: str):
        """Inicializa los atributos de la clase.

        Args:
            host (str): El host de la base de datos.
            port (str): El puerto de la base de datos.
            user (str): El nombre de usuario para conectarse a la base de datos.
            password (str): La contraseña para conectarse a la base de datos.
            database_name (str): El nombre de la base de datos existente ya en el servidor mysql.
        """
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.database_name = database_name
        self.conn = self.connect()


    def connect(self) -> pymysql.connections.Connection:
        """Intenta establecer una conexión con la base de datos.

        Si la conexión se realiza con éxito, muestra un mensaje de éxito. Si ocurre un error al conectarse, muestra un
        mensaje de error.
        """
        try:
            self.conn = pymysql.Connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.password,
                db=self.database_name
            )
            return self.conn
        
        except Exception as e:
            logging.error(f"Error al conectar a base de datos: {str(e)}")
            raise FailConect("No se pudo establecer una conexión con la base de datos")
            
    
    
    def close(self) -> None:
        """Intenta cerrar la conexión con la base de datos.

        Si la conexión se cierra con éxito, muestra un mensaje de éxito. Si ocurre un error al cerrar la conexión, muestra
        un mensaje de error.
        """
        try:
            self.conn.close()
            self.conn= None
        except Exception as e:
            logging.error(f"Error al cerrar conexión: {str(e)}")
            raise FailConect(f"Ocurrio un error : {str(e)} ")
    
    def cursor_execute_command(self,*args) -> tuple or None :
        """
        Crea un cursor y ejecuta los comandos que se le pasen como argumentos.
        Este método se usa para ejecutar comandos de tipo DDL (Data Definition Language)
        como CREATE, ALTER, DROP, TRUNCATE, RENAME, etc.

        Este método será usado por otros métodos de la clase DataBase.

        Args:
            *args (str): Uno o más comandos a ejecutar.

        Returns:
            objeto (tuple o None): Retorna la respuesta al último comando ejecutado,
                siendo None en caso de que no haya respuesta ya que el comando no devuelve nada.
                o una tupla con los datos de la consulta por ejemplo al hacer "SELECT * FROM tabla"

        Raises:
            FailConect: Si se produce un error al ejecutar los comandos.
        """
        try:
            cursor=self.conn.cursor()
            for arg in args:
                cursor.execute(arg)
                objeto=cursor.fetchall()
            self.conn.commit()
            cursor.close()
            return objeto
        except Exception as e:
            logging.error(f"Error al ejecutar comando: {str(e)}")
            raise FailConect(f"Error de comandos : {str(e)} ")
            
    
    
    def drop_table(self, name_table) -> None:
        """Se eliminará una tabla especificada dentro de la base de datos."""
        try:
            command= f"""DROP TABLE IF EXISTS {name_table}"""
            self.cursor_execute_command(command)
            
        except Exception as e:
            logging.error(f"Error al eliminar tabla: {str(e)}")
            raise FailConect(f"Ocurrio un error : {str(e)} ")
            
            
    def create_table(self, name_table:str, fields_data:str) -> None:
        """Se creará una tabla dentro de la base de datos.
            En caso la tabla ya exista, se eliminará y se creará nuevamente.
        
        Args:
            name_table (str): Nombre de la tabla a crear.
            fields_data (str): Campos de la tabla a crear.
        
        """
        try:
            self.drop_table(name_table)
            command= f"""CREATE TABLE {name_table} ({fields_data}) """
            self.cursor_execute_command(command)
        
        except Exception as e:
            logging.error(f"Error al crear tabla: {str(e)}")
            raise FailConect(f"Ocurrio un error : {str(e)} ")
    
    def insert_into_table(self, name_table:str, columns : list[str], values: list[tuple]):
        """
        Inserta una serie de valores en una tabla determinada.

        Args:
            table_name (str): Nombre de la tabla en la que se insertarán los valores.
            columns (List[str]): Lista de nombres de las columnas en las que se insertarán los valores.
            values (List[tuple]): Lista de tuplas con los valores a insertar en las columnas correspondientes.

        Returns:
            None
        """
        
        
        try:
            insert_query_list = []
            for value in values:
                insert_query = f"INSERT INTO {name_table} ({','.join(columns)}) VALUES {value}"
                insert_query_list.append(insert_query)
            self.cursor_execute_command(*insert_query_list)
            
        except Exception as e:
            logging.error(f"Error al insertar datos: {str(e)}")
            raise FailConect(f"Ocurrio un error : {str(e)} ")
    
    def select_from_table(self, name_table:str, columns : list[str] = None, where : str = None) -> list[tuple]:
        """
        Selecciona una serie de valores de una tabla determinada.

        Args:
            table_name (str): Nombre de la tabla de la que se seleccionarán los valores.
            columns (List[str]): Lista de nombres de las columnas de las que se seleccionarán los valores.
            where (str, optional): Condición para filtrar los valores. Defaults to None.

        Returns:
            List[tuple]: Lista de tuplas con los valores seleccionados.
        """
        try:
            if columns:
                select_query = f"SELECT {','.join(columns)} FROM {name_table}"
            select_query= f"SELECT * FROM {name_table}"
            if where:
                select_query += f" WHERE {where}"
            return self.cursor_execute_command(select_query)
        except Exception as e:
            logging.error(f"Error al seleccionar datos: {str(e)}")
            raise FailConect(f"Ocurrio un error : {str(e)} ")
    
    def update_table(self, name_table:str, columns : list[str], values : list[str], where : str = None):
        """
        Actualiza una serie de valores de una tabla determinada, si el where es específico 
        sólo se actualiza la(s) fila(s) que cumplan con el criterio.
        De lo contrario,o en caso el where no sea específicado, se alteran todas las filas con los valores
        señalados.

        Args:
            table_name (str): Nombre de la tabla en la que se actualizarán los valores.
            columns (List[str]): Lista de nombres de las columnas en las que se actualizarán los valores.
            values (List[str]): Lista de valores a actualizar en las columnas correspondientes.
            where (str, optional): Condición para filtrar las o la fila a modificar. Defaults to None.

        Returns:
            None
            
        Raises:
            FailConect: Error al actualizar datos.
        """
        
        def add_quotes(obj):
            """Agrega comillas simples a un objeto si este es de tipo str.
                Devuelve 'NULL' si el objeto es None, 'null' o una cadena vacía.

            Args:
                obj (object): Objeto a evaluar.

            Returns:
                'NULL' si el objeto es None, 'null' o una cadena vacía.
                str or object: Si el objeto es una cadena de texto, se agrega comillas extras internas.
            """
            Null_list = [None, 'None', 'none', 'NULL', 'null', 'Null','']
            if obj in Null_list:
                return 'NULL'
            if isinstance(obj, str):
                return f"'{obj}'"
            return obj
        
        try:
            update_query_list = []
            for column, value in zip(columns, values):
                update_query = f"UPDATE {name_table} SET {column} = {add_quotes(value)}"
                if where:
                    update_query += f" WHERE {where}"
                update_query_list.append(update_query)
            self.cursor_execute_command(*update_query_list)
        except Exception as e:
            logging.error(f"Error al actualizar datos: {str(e)}")
            raise FailConect(f"Ocurrio un error : {str(e)} ")
    
    
    def delete_from_table(self, name_table: str, where :str) -> None:
        """Función que permite eliminar filas de una tabla, de acuerdo a la sentencia where

        Args:
            name_table (str): Nombre de la tabla de la que se eliminarán los valores.
            where (str): Sentencia de filtro para eliminar filas.

        Raises:
            FailConect: Error al eliminar datos.
        """
        try:
            query = f"DELETE FROM {name_table} WHERE {where}"
            self.cursor_execute_command(query)
        except Exception as e:
            logging.error(f"Error al eliminar datos: {str(e)}")
            raise FailConect(f"Ocurrio un error : {str(e)} ")
        
    
    def from_dataframe_create_table(self, name_table:str, df: pd.DataFrame) -> bool:
        """Función que permite crear una tabla a partir de un dataframe.
            Si la tabla ya existe, se eliminará y se creará nuevamente.
        
        Args:
            name_table (str): Nombre de la tabla a crear.
            df (pd.DataFrame): Dataframe a partir del cual se creará la tabla.
        
        Raises:
            FailConect: Error al crear tabla.
        """
        try:
            #Elimina la tabla en caso de existir
            self.drop_table(name_table)
            
            # Dtype to MySQL type
            mysql_types = {'object': 'VARCHAR(255)',
                       'int64': 'INT',
                       'float64': 'FLOAT',
                       'datetime64': 'DATETIME'}
            
            #Crea una lista con los nombres de la columna y el tipo de datos en mysql
            columns = df.columns.tolist()
            types = df.dtypes.tolist()
            table= []
            for column, _type in zip(columns, types):
                table.append((column, mysql_types[str(_type)]))
            
            #Crea el var_field para crear la tabla
            field_columns=""
            for columna in table:
                field_columns += columna[0] + " " + columna[1] + ",\n"
            field_columns=field_columns[:-2]
            
            #Crea la tabla
            self.create_table(name_table=name_table, fields_data=field_columns)
            #Insertar los valores del dataframe en una tabla
            self.insert_into_table(name_table=name_table, columns=columns, values=df.to_records(index=False))
            
            #Retornar el resultado de la consulta
            return True
            
            
        except Exception as e:
            logging.error(f"Error al crear tabla: {str(e)}")
            raise FailConect(f"Ocurrio un error : {str(e)} ")
        
    
    def consultar_id_and_return_json(self,id:str):
        """
        Función específica para base de datos de proyecto Wedding_card
        Consultar a base de datos por un id y retornar un json con los datos especificados

        Args:
            id (str): id de consulta para obtener datos

        Raises:
            FailConect: 
        Returns:
            JSON : json con los datos de la consulta
        """
        try:
            data=self.select_from_table(name_table="Lista_de_invitados",where=f"ID='{id}'")
            result = {"ID": data[0][0], "SEX": data[0][1], "APELLIDOS": data[0][2], "NOMBRES": data[0][3], "NUMBER_GUEST": data[0][4], "MESA": data[0][5], "CELULAR": data[0][6], "CONFIRMADO": data[0][7]}
            json_data = json.dumps(result)
            return json_data
        except Exception as e:
            logging.error(f"Error al consultar datos: {str(e)}")
            raise FailConect(f"Ocurrio un error : {str(e)} ")