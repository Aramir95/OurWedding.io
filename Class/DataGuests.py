import pandas as pd
import openpyxl
import os
import random
import string
from Class.DataExcel import DataExcel

class DataGuests(DataExcel):
    
    def __init__(self):
        self._path=self.find_path_guest_file()
        super().__init__(path=self._path,header="ID")
        self.save_path= self._path
        self._frame=self.reload_excel()
        
    
    def find_path_guest_file(self)-> str:
        """
        Busca el archivo de invitados en la carpeta Data.

        Returns:
            str: Ruta del archivo de invitados.
        """
        path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"Data","guest.xlsx")
        return path
    
    def find_path_data_wsp(self)-> str:
        """
        Busca y crea la ruta de archivo para envío de invitados por WhatsApp.

        Returns:
            str: Ruta del archivo de invitados.
        """
        path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"Data","wsp_status.xlsx")
        return path
    
    def save_wsp_data(self):
        self._frame.to_excel(self.find_path_data_wsp(),index=False)
        return True
    

    
    def reload_excel(self)-> pd.DataFrame:
        """Función que actualiza el archivo de invitados con ID's aleatorios en caso de que estén vacíos.
        Guarda los cambios en el archivo fuente y devuelve el dataframe actualizado con todas las celdas en formato str. 


        Returns:
            pd.DataFrame: Dataframe actualizado.
        """
        
        dataframe=self.load_excel()
        dataframe=dataframe.dropna(subset=["APELLIDOS"])
        dataframe=dataframe.fillna("")
        
        def generate_id(cell_value:str)-> str:
            """Función que devuelve un ID de 6 caracteres alfanuméricos.

            Args:
                cell_value (str): ID por defecto de la celda, se modifica si está vacío.

            Returns:
                str: Nuevo ID en caso la celda esté vacía, o el ID por defecto de la celda.
            """
            
            if cell_value == "":
                while True:
                    new_id="".join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    if new_id not in dataframe["ID"].values:
                        return new_id
            else:
                return cell_value
            
        
        dataframe["ID"]=dataframe["ID"].apply(generate_id)
        dataframe = dataframe.applymap(lambda s: s.upper() if type(s) == str else s)
        dataframe.to_excel(self.save_path,index=False)
        dataframe=pd.read_excel(self.save_path,dtype=str)
        dataframe=dataframe.fillna("NULL")
        dataframe=dataframe.replace("","NULL")
        dataframe=dataframe.replace("none","NULL")
        dataframe=dataframe.replace("None","NULL")
        return dataframe
    
    
    
    def apply_function_to_rows(self, func):
        """
        
        Toma una función y la aplica a cada fila del dataframe. El resultado de la función se agrega en una nueva columna
        al final del dataframe con el nombre de la función como header.
        
        Args:
            func (callable): Función a aplicar a cada fila del DataFrame.
            
        Returns:
            pandas.DataFrame: Dataframe original con una nueva columna que contiene los resultados de la función.
        """
        # Convertimos el DataFrame a un array de numpy para mejorar la velocidad
        np_array = self._frame.values
        
        # Creamos una lista vacía para almacenar los resultados
        results = []
        
        # Iteramos sobre cada fila del array y aplicamos la función a cada una de ellas
        for row in np_array:
            result = func(*row)
            results.append(result)
        
        # Creamos una nueva columna en el DataFrame con los resultados
        func_name = func.__name__
        self._frame[func_name] = results
        
        return self._frame