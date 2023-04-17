import pandas as pd
import os
from dotenv import load_dotenv
import mysql.connector
from sshtunnel import SSHTunnelForwarder

load_dotenv()

def connectToDatabase():
    tunnel = SSHTunnelForwarder(
        (os.getenv('SSH_HOST'), int(os.getenv('SSH_PORT'))),
        ssh_username=os.getenv('SSH_USER'),
        ssh_password=os.getenv('SSH_PASSWORD'),
        remote_bind_address=(os.getenv('REMOTE_HOST'), int(os.getenv('REMOTE_PORT'))),
        local_bind_address=(os.getenv('LOCAL_HOST'), int(os.getenv('LOCAL_PORT')))
    )
    tunnel.start()

    db = mysql.connector.connect(
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=tunnel.local_bind_port,
        database=os.getenv('DATABASE_NAME')
    )

    return db, tunnel

def getLinksToDownload():
    db, tunnel = connectToDatabase()
    cursor = db.cursor()

    sql = """SELECT  mme.id, mme.managemeetid, mm.course, cc.id,cc.name, mc.shortname, mc.fullname,   mme.name, mme.intro, mme.time, mme.timehasta,
        DATE_FORMAT(FROM_UNIXTIME(mme.time),'%%Y-%%m-%%d %%H:%%i:%%S') AS 'fechainicio',
        DATE_FORMAT(FROM_UNIXTIME(mme.timehasta),'%%Y-%%m-%%d %%H:%%i:%%S') AS 'fechafin',
        mme.webinar, mme.record, mme.new_url,
        DATE_FORMAT(FROM_UNIXTIME(mme.timecreated),'%%Y-%%m-%%d %%H:%%i:%%S') AS 'fechacread'
        FROM mdl_managemeet_event mme
        JOIN mdl_managemeet mm ON mm.id =mme.managemeetid
        JOIN mdl_course mc ON mc.id =mm.course
        JOIN mdl_course_categories AS cc ON mc.category = cc.id
        WHERE mme.record like '%%https://comfama.webex.com%%'
        and mme.timecreated >= 1672549200
        AND cc.id in (216)"""

    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print('Error en la consulta: {}'.format(err))
        return None
    finally:
        db.close()
        tunnel.stop()

def updateLinks(result):
    db, tunnel = connectToDatabase()
    cursor = db.cursor()

    for row in result:
        mgmeet_record = row[15]
        new_url = row[14]

        sql = "UPDATE mdl_managemeet_event SET new_url = %s WHERE record = %s"
        val = (new_url, mgmeet_record)

        try:
            cursor.execute(sql, val)
            print('se actualizó ' + new_url)
        except mysql.connector.Error as err:
            print('No se encontró en la base de datos: {}'.format(err))
        finally:
            db.commit()

    db.close()
    tunnel.stop()
