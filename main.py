import os

from dotenv import load_dotenv

from postgres import PostgresConnection
from remote import SSHConnection
from zabbix_setter import ZabbixHostNameSetter

load_dotenv()


def main():
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_port = os.getenv('DB_PORT')
    postgres_connection = PostgresConnection(db_host=db_host, db_name=db_name, db_user=db_user,
                                             db_password=db_password, db_port=db_port)
    postgres_connection.connect()
    setter = ZabbixHostNameSetter(connection=postgres_connection)
    setter.run_for_certain_host_id(host_id=10582)
