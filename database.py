import pandas as pd
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def updateLinks(df):
    db = mysql.connector.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USERTEST'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE')
    )
    
    for index, row in df.iterrows():

        mgmeet_record = row['Mgmeet record']
        new_url = row['new_url']

        cursor = db.cursor()
        sql = "UPDATE mdl_managemeet_event SET new_url = %s WHERE record = %s"
        val = (new_url, mgmeet_record)
        cursor.execute(sql, val)
        db.commit()
    db.close()