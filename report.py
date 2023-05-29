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

today = datetime.now().strftime("%Y-%m-%d")
body = f"El contenedor {container.container_name} tiene {count} blobs, después del proceso de carga ejecutado hoy ({today})."
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')
sender_email = os.getenv('SENDER_EMAIL')
receiver_email = os.getenv('RECEIVER_EMAIL')


msg = MIMEText(body)
msg['Subject'] = 'Conteo de blobs en Azure Blob Storage'
msg['From'] = sender_email
msg['To'] = receiver_email

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, [receiver_email], msg.as_string())

