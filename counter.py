from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
container = blob_service_client.get_container_client(os.getenv('AZURE_STORAGE_CONTAINER_NAME'))

count = 0
for blob in container.list_blobs():
    count += 1

print(f"El contenedor {container.container_name} tiene {count} blobs.")
