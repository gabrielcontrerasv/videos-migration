import pandas as pd
from sshtunnel import SSHTunnelForwarder
import os
import paramiko
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_links():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=os.getenv('SSH_HOST'),
                username=os.getenv('SSH_USER'),
                password=os.getenv('SSH_PASSWORD'))

    comando_mysql = "mysql -u " + os.getenv('DATABASE_USER') + " -p" + os.getenv('DATABASE_PASSWORD') + " -h " + os.getenv('DATABASE_HOST') + " -D " + os.getenv('DATABASE_NAME') + " -e \"SELECT mme.record FROM mdl_managemeet_event mme JOIN mdl_managemeet mm ON mm.id =mme.managemeetid JOIN mdl_course mc ON mc.id =mm.course JOIN mdl_course_categories AS cc ON mc.category = cc.id WHERE mme.record like '%https://comfama.webex.com%' and mme.timecreated >= 1672549200 AND cc.id in (216) AND mme.new_url Is null;\""
    stdin, stdout, stderr = ssh.exec_command(comando_mysql)
    result = stdout.read().decode('utf-8')

    ssh.close() 
    return convert_to_dataframe(result)

def convert_to_dataframe(result):
    resultados = result.strip().split("\n")[1:]
    filas = [fila.split("\t") for fila in resultados]
    return pd.DataFrame(filas, columns=["record"])

def update_links(result):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=os.getenv('SSH_HOST'),
                username=os.getenv('SSH_USER'),
                password=os.getenv('SSH_PASSWORD'))

    comando_mysql = "mysql -u " + os.getenv('DATABASE_USER') + " -p" + os.getenv('DATABASE_PASSWORD') + " -h " + os.getenv('DATABASE_HOST') + " -D " + os.getenv('DATABASE_NAME') + " -e \""
    for index, row in result.iterrows():
        mgmeet_record = row['record']
        new_url = row['new_url']

        sql = "UPDATE mdl_managemeet_event SET new_url = '" + new_url + "' WHERE record = '" + mgmeet_record + "';"
        comando_mysql += sql

    stdin, stdout, stderr = ssh.exec_command(comando_mysql)
    print(stdout.read().decode('utf-8'))

    ssh.close()
