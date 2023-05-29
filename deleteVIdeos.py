import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import pandas as pd
from datetime import datetime
load_dotenv()


connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
output_file = "informe_videos_eliminados.xlsx"


def delete_container_videos(connection_string, container_name, output_file):
    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blobs()

    data = []
    for blob in blobs:
        container_client.delete_blob(blob.name)
        data.append([blob.name, datetime.now()])

    df = pd.DataFrame(data, columns=['Archivo', 'Fecha de eliminación'])
    df.to_excel(output_file, index=False)

    print("Se han eliminado todos los blobs del contenedor:", container_name)
    print("Los nombres de los archivos eliminados se han guardado en:", output_file)


delete_container_videos(connection_string, container_name, output_file)
