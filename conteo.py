import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

load_dotenv()

blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
container = blob_service_client.get_container_client(os.getenv('AZURE_STORAGE_CONTAINER_NAME'))

count = 0
for blob in container.list_blobs():
    count += 1
print(count)    