import requests
import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import time

load_dotenv()

time.sleep(10)

# Accede a la variable de entorno CLASES_FILE
clases = os.getenv('CLASES_FILE')

# Obtenemos la ruta del directorio actual y concatenamos /clases
download_path = os.path.join(os.getcwd(), 'clases')

# Cargamos el archivo de Excel que contiene las URLs de los videos
df = pd.read_excel('clases.xlsx')
videos = []

driver = webdriver.Remote(
   command_executor='http://selenium-hub:4444/wd/hub',
   options=webdriver.ChromeOptions()
   )
  
try:
    #driver.implicitly_wait(30)
    driver.maximize_window() # Note: driver.maximize_window does not work on Linux selenium version v2, instead set window size and window position like driver.set_window_position(0,0) and driver.set_window_size(1920,1080)
    for url in df['Mgmeet record']:
        # Abrimos la URL en el navegador
        driver.get(url)
        time.sleep(5)
        # Hacemos clic en el botón de descarga
        driver.execute_script("document.querySelector('i').click()")
        time.sleep(2)
        iframe = driver.find_element("css selector", '#iframe_MP4')
        if iframe:
            videos.append(iframe.get_attribute("src"))
finally:
    driver.quit()



for index, link in enumerate(videos):

		# obtain the filename by splitting the URL 
		name_of_file = download_path + "/" + str(index + 1) + "_.mp4"

		print( "Downloading file:%s"%name_of_file)
		
		# create a response object
		response = requests.get(link, stream = True)
		
		# download started
		with open(name_of_file, 'wb') as f:
			for chunk in response.iter_content(chunk_size = 1024*1024):
				if chunk:
					f.write(chunk)

		
		print( "%s downloaded!\n"%name_of_file )


blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))

# Definimos el nombre del contenedor de Blob Storage donde queremos almacenar los archivos
container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')

while True:
    if all(file.endswith('.mp4') for file in os.listdir(download_path)):
        break
    time.sleep(1)
    print('Esperando a que se descargue el archivo...')
print('subiendo a azureBlob...')
# Subimos el archivo descargado a Azure Blob Storage
for file in os.listdir(download_path):
    if file.endswith('.mp4'):
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file)
        with open(os.path.join(download_path, file), "rb") as data:
            print("ya estoy enviando paquetes")
            blob_client.upload_blob(data, overwrite=True)
            print("ya termine, eliminando...")
        # Borramos el archivo descargado
        os.remove(os.path.join(download_path, file))

