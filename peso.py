import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
container = blob_service_client.get_container_client(os.getenv('AZURE_STORAGE_CONTAINER_NAME'))

total_size = 0

for blob in container.list_blobs():
    total_size += blob.size

print(f"El peso total de los archivos en el contenedor {os.getenv('AZURE_STORAGE_CONTAINER_NAME')} es {total_size} bytes.")
