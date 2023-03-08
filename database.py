import pandas as pd
import os
from dotenv import load_dotenv
import mysql.connector
from sshtunnel import SSHTunnelForwarder

load_dotenv()

def updateLinks(df):
    with SSHTunnelForwarder(
        (os.getenv('SSH_HOST'), 22),
        ssh_username=os.getenv('SSH_USER'),
        ssh_password=os.getenv('SSH_PASSWORD'),
        remote_bind_address=('127.0.0.1', 3306),
        local_bind_address=('127.0.0.1', 3307)
    ) as tunnel:
        db = mysql.connector.connect(
            user=os.getenv('DATABASE_USER'), password=os.getenv('DATABASE_PASSWORD'),
            host='127.0.0.1', port=tunnel.local_bind_port,
            database=os.getenv('DATABASE')
        )

        for index, row in df.iterrows():
            mgmeet_record = row['Mgmeet record']
            new_url = row['new_url']

            cursor = db.cursor()
            sql = "UPDATE mdl_managemeet_event SET new_url = %s WHERE record = %s"
            val = (new_url, mgmeet_record)
            try:
                cursor.execute(sql, val)
                print('se se actualizo' + new_url)
            except:
                print('no lo encontre en base de datos')
                continue    
            db.commit()

        db.close()
