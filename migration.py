import pandas as pd
import os
import time
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import updateLinks

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Accede a la variable de entorno CLASES_FILE
clases = os.getenv('CLASES_FILE')

# Obtenemos la ruta del directorio actual y concatenamos /clases
download_path = os.path.join(os.getcwd(), 'clases')

# Cargamos el archivo de Excel que contiene las URLs de los videos
df = pd.read_excel(clases)

# Configuramos las opciones de Firefox para descargar los archivos automáticamente en modo headless
options = Options()
options.add_argument('-headless')
prefs = {'download.default_directory': download_path}
options.set_preference('browser.download.folderList', 2)
options.set_preference('browser.download.manager.showWhenStarting', False)
options.set_preference('browser.download.dir', download_path)
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'video/mp4')

# Inicializamos el driver de Firefox
driver = webdriver.Firefox(options=options)

# Creamos una instancia del cliente de Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))

# Definimos el nombre del contenedor de Blob Storage donde queremos almacenar los archivos
container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
blob_urls = []
# Iteramos sobre cada URL en el archivo de Excel
for url in df['Mgmeet record']:
    # Abrimos la URL en el navegador
    driver.get(url)
    time.sleep(2)
    # Hacemos clic en el botón de descarga
    download_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'i.recordingDownload[title="Descargar"]')))
    print('descargando porfavor espere...')
    download_button.click()
    time.sleep(2)

    # Esperamos a que se descargue el archivo antes de continuar
    while True:
        if all(file.endswith('.mp4') for file in os.listdir(download_path)):
            break
        print('Esperando a que se descargue el archivo...')
    print('subiendo a azureBlob...')
    # Subimos el archivo descargado a Azure Blob Storage
    for file in os.listdir(download_path):
            blob_url = f"https://{os.getenv('AZURE_STORAGE_ACCOUNT')}.blob.core.windows.net/{container_name}/{file}"
            blob_urls.append(blob_url)
            print("ya estoy enviando paquetes")
            cmd = '''az storage blob upload \
            --account-name sagrabacionescursos \
            --container-name videos \
            --name "'''+file+'''" \
            --file "clases/'''+file+'''" \
            --overwrite \
            --auth-mode login
            '''
            print(cmd)
            os.system(cmd)
            print("ya termine ...")
            os.remove(os.path.join(download_path, file))
df = df.assign(new_url=blob_urls)
# Nombre del archivo de Excel
excel_file = 'resultado.xlsx'
# Guardamos el DataFrame en el archivo de Excel
df.to_excel(excel_file, index=False)
# Cerramos el navegador
driver.quit()
print('actualizando base de datos')
updateLinks(df)
print('registros actualizados correctamente')