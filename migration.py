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
from database import connectToDatabase,getLinksToDownload,updateLinks
import log
import datetime

logger = log.getLog()
#conectar a la vpn
#cmd = "./vpn.sh"
#os.system(cmd)


load_dotenv()
clases = getLinksToDownload()
sas = os.getenv('SAS')
account = os.getenv('AZURE_STORAGE_ACCOUNT')
download_path = os.path.join(os.getcwd(), 'clases')

options = Options()
options.binary_location = r'/usr/bin/firefox-esr'
options.add_argument('-headless')
prefs = {'download.default_directory': download_path}
options.set_preference('browser.download.folderList', 2)
options.set_preference('browser.download.manager.showWhenStarting', False)
options.set_preference('browser.download.dir', download_path)
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'video/mp4')

driver = webdriver.Firefox(options=options)
blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
blob_urls = []
for url in clases['Mgmeet record']:
    try:
        driver.get(url)
        time.sleep(2)
        download_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.recordingHeader i')))
        print('descargando porfavor espere...')
        logger.info(f"Descargando video de la URL: {url}")
        download_button.click()
        time.sleep(2)

        while True:
            if all(file.endswith('.mp4') for file in os.listdir(download_path)):
                break
            print('Esperando a que se descargue el archivo...')
        print('subiendo a azureBlob...')
        logger.info(f"Subiendo video de la URL: {url} a azureBlob")
        for file in os.listdir(download_path):
                blob_url = f"https://{os.getenv('AZURE_STORAGE_ACCOUNT')}.blob.core.windows.net/{container_name}/{file}"
                blob_urls.append(blob_url)
                print("ya estoy enviando paquetes")
                cmd = f'''az storage blob upload \
                --account-name {account} \
                --container-name {container_name} \
                --name "{file}" \
                --file "clases/{file}" \
                --overwrite \
                --sas-token "{sas}"
                '''
                os.system(cmd)
                print("ya termine ...")
                logger.info(f"Finalizacion de subida del video de la URL: {url} a azureBlob")
                logger.info(f"Eliminando video de la URL: {url}")
                os.remove(os.path.join(download_path, file))
                logger.info(f"Video eliminado de la URL: {url}")
    except Exception as e:
        print(f"Ocurrió un error en la descarga de la URL {url}: {str(e)}")
        logger.error(f"Ocurrió un error en la descarga de la URL {url}: {str(e)}")
        now = datetime.datetime.now()
        date_string = now.strftime('%Y-%m-%d_%H-%M-%S')
        driver.save_screenshot(f'screenshots/screenshots_{date_string}.png')
        blob_urls.append('')
        continue
results = clases.assign(new_url=blob_urls)
results.to_excel('resultado.xlsx', index=False)
driver.quit()
updateLinks(results)
