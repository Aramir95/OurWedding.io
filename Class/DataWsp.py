import pandas as pd
import openpyxl
import os
import re
import datetime
from Class.DataExcel import DataExcel
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


class DataWsp(DataExcel):
    
    def __init__(self):
        self._path=self.find_path_to_wsp_file()
        super().__init__(path=self._path,header="ID")
        self._frame=self.load_excel()
        self.driver=None
        
    def find_path_to_wsp_file(self)-> str:
        """
        Busca el archivo de invitados en la carpeta Data.

        Returns:
            str: Ruta del archivo de invitados.
        """
        
        path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"Data",f"to_wsp.xlsx")
        return path
    
        
    def path_save_wsp_data(self)-> str:
        """
        Busca y crea la ruta de archivo para envío de invitados por WhatsApp.

        Returns:
            str: Ruta del archivo de invitados.
        """
        hora_actual = datetime.datetime.now().strftime('%Y%m%d-%H%M')
        path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"Data",f"wsp_status__{hora_actual}.xlsx")
        return path
    
    def load_excel(self):
        dataframe=pd.read_excel(self._path,dtype=str)
        return dataframe
    
    def save_wsp_data(self):
        self._frame.to_excel(self.path_save_wsp_data(),index=False)
        return True
    
    
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
    
    def init_selenium_wsp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://web.whatsapp.com/')
        input("Escanea el código QR y presiona Enter")
        return True   

    @staticmethod
    def procesar_celular(texto):
        """
        Toma un texto que contiene uno o varios números de celular separados por punto y coma, y devuelve una lista de 
        números de celular con el prefijo '+51' agregado.
        
        Args:
            texto (str): Texto que contiene uno o varios números de celular separados por punto y coma.
            
        Returns:
            list: Lista de números de celular con el prefijo '+51' agregado.
            
            False: Si el texto es None, tiene menos de 6 caracteres o es igual a una de las cadenas "NULL", "none" o "None".
        """
        if not texto or len(texto) < 6 or texto.lower() in ["null", "none","nan"]:
            # Si el texto es None, tiene menos de 6 caracteres o es igual a una de las cadenas "NULL", "none" o "None",
            # devolver False
            return False
        
        numeros = re.findall(r'\d+', texto)
        if not numeros:
            # Si no se encontró ningún número en el texto, devolver False
            return False
        
        numeros_con_prefijo = [f'+51{numero}' for numero in numeros]
        return numeros_con_prefijo
    
    
    
    
    def send_message_from_selenium(self,num_celular:list, mensajes:list):
        
        def paste_content(driver, el, content):
            driver.execute_script(
            f'''
        const text = `{content}`;
        const dataTransfer = new DataTransfer();
        dataTransfer.setData('text', text);
        const event = new ClipboardEvent('paste', {{
        clipboardData: dataTransfer,
        bubbles: true
        }});
        arguments[0].dispatchEvent(event)
        ''',
            el)
            
        time.sleep(5)
        for num in num_celular:
            url = f"https://web.whatsapp.com/send?phone={num}"
            self.driver.get(url)
            WebDriverWait(self.driver, 600).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')))
            time.sleep(5)
            for mensaje in mensajes:
                input_box = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
                paste_content(self.driver, input_box, mensaje)
                input_box.send_keys(Keys.ENTER)
                time.sleep(2)
            
            print(f"Se envió mensaje completo a {num}")
            
        
        return "Se envió mensaje wsp"
    
    
    
    def crear_mensajes_del_novio_por_fila(self,id, sex, apellidos, nombres, number_gest, mesa, celular, msj,*args):
        try:
            # Generar el mensaje de WhatsApp
            if sex == "F":
                if number_gest == "1":
                    mensaje1 = f"""🎊 Querida *{apellidos} {nombres}*, 🎊 tiene  *{number_gest}* silla reservada en la mesa *{mesa}* 🪑de nuestra recepción 🎉
    ¡Los esperamos hoy en nuestra boda! 🤵👰 Por favor, visiten la web para más detalles 🌐
    Ingresando el código secreto y dando click en enviar  📤:

                    """
                else:
                    mensaje1 = f"""🎊 Querida *{apellidos} {nombres}*, 🎊 tiene  {number_gest} sillas reservada en la mesa *{mesa}* 🪑de nuestra recepción 🎉

    ¡Los esperamos hoy en nuestra boda! 🤵👰 Por favor, visiten la web para más detalles 🌐
    Ingresando el código secreto y dando click en enviar  📤:
    """
            elif sex == "M":
                if number_gest == "1":
                    mensaje1 = f"""🎊 Querido *{apellidos} {nombres}*,  🎊 tiene  {number_gest} silla reservada en la mesa *{mesa}* 🪑de nuestra recepción 🎉
    ¡Los esperamos hoy en nuestra boda! 🤵👰 Por favor, visiten la web para más detalles 🌐
    Ingresando el código secreto y dando click en enviar  📤:
                    """
                else:
                    mensaje1 = f"""🎊 Querido *{apellidos} {nombres}*, 🎊 tiene  *{number_gest}* sillas reservada en la mesa *{mesa}* 🪑 de nuestra recepción 🎉
     ¡Los esperamos hoy en nuestra boda! 🤵👰 Por favor, visiten la web para más detalles 🌐
    Ingresando el código secreto y dando click en enviar  📤:       
                    """
            
            mensaje2 = f"🔗https://aramir95.github.io/OurWedding.io/"

            mensaje3= f"El código secreto 🔒 es:"
            mensaje4 = f"{id}"
            mensaje5 = f"""📍 Boda Religiosa
⛪ Iglesia Evangélica Peregrina
📌 Nicolás de Piérola 565, Barranca
⏰ 03:00 PM - 04:00 PM
🗺️ https://www.google.com/maps/dir/?api=1&destination=Nicol%C3%A1s%20de%20Pi%C3%A9rola%20565%2C%20Barranca%2015169

📍 Recepción y Fiesta
🏡 CASA BLANCA - GORRIONCITO
📌 Urb. La Florida Mz. R Lt. 14/ Calle Miguel Grau
⏰ 05:30 PM - Hasta que el cuerpo aguante 🕺💃
🗺️ https://www.google.com/maps/dir/?api=1&destination=-10.7288611,-77.77438889999999
Tiene  *{number_gest}* silla(s) reservada(s) en la mesa *{mesa}* 🪑 del local *CASA BLANCA - GORRIONCITO* 🏡

¡Esperamos verlos allí! 🥳🥂💕"""

            mensajes = [mensaje1, mensaje2, mensaje3, mensaje4, mensaje5]
            return mensajes

    
        except Exception:
            raise Exception("No se pudo crear el mensaje")
        
    def crear_mensajes_de_novia_por_fila(self,id, sex, apellidos, nombres, number_gest, mesa, celular, msj,*args):
        mensajes=self.crear_mensajes_del_novio_por_fila(id, sex, apellidos, nombres, number_gest, mesa, celular, msj,*args)
        mensajes[0]=mensajes[0].replace("Soy Angel y junto a Wendy 🤵‍♂️👰","Soy Wendy y junto a Angel 👰🤵‍♂️")
        return mensajes
        
    
    def message_from_data_in_row_selenium(self,id, sex, apellidos, nombres, number_gest, mesa, celular, msj,*args):
        # Procesar el número de celular
        num_celular = self.procesar_celular(celular)
        
        # Verificar que se pudo procesar el número de celular
        if not num_celular:
            return "No se pudo enviar wsp"
        
        try:
            mensajes=self.crear_mensajes_del_novio_por_fila(id, sex, apellidos, nombres, number_gest, mesa, celular, msj,*args)
            mensajes.insert(0, ".")
            self.send_message_from_selenium(num_celular, mensajes)
            return "Se envió wsp"
        except Exception as e:
            return f"No se pudo enviar wsp - problema al ejecutar: {e}"
    
        
    
    def MultipleMessageFromDataInRowSelenium(self):
        self.init_selenium_wsp()
        self.apply_function_to_rows(self.message_from_data_in_row_selenium)
        self.save_wsp_data()
        self.driver.quit()
        self.driver=None
        return True
    

#Documenta y optimiza todo el código de este documento