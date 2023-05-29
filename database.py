import pandas as pd
import os
import pandas as pd
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def get_links():
    db = mysql.connector.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USERTEST'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE')
    )
    
    cursor = db.cursor()
    sql = """SELECT
	mme.record
FROM
	mdl_managemeet_event mme
JOIN mdl_managemeet mm ON
	mm.id = mme.managemeetid
JOIN mdl_course mc ON
	mc.id = mm.course
JOIN mdl_course_categories AS cc ON
	mc.category = cc.id
WHERE
	mme.record like '%https://comfama.webex.com%'
	and mme.timecreated >= 1672549200
	AND cc.id in (216)
	AND (mme.new_url Is null OR mme.new_url = '') limit 1;"""

    cursor.execute(sql)
    result = [row for row in cursor]
    print(result)
    db.close()

    return convert_to_dataframe(result)

def convert_to_dataframe(result):
    return pd.DataFrame(result, columns=["record"])

def update_links(df):
    db = mysql.connector.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USERTEST'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE')
    )

    for index, row in df.iterrows():

        mgmeet_record = row['record']
        new_url = row['new_url']

        cursor = db.cursor()
        sql = "UPDATE mdl_managemeet_event SET new_url = %s WHERE record = %s"
        val = (new_url, mgmeet_record)
        cursor.execute(sql, val)
        db.commit()
    db.close()
