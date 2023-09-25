import os

from dotenv import load_dotenv

from postgres import PostgresConnection
from zabbix_setter import ZabbixHostNameSetter

load_dotenv()


class Main:
    def __init__(self):
        self.zabbix_host_name_setter = None

    @staticmethod
    def get_postgres_connection():
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_port = os.getenv('DB_PORT')
        postgres_connection = PostgresConnection(db_host=db_host, db_name=db_name, db_user=db_user,
                                                 db_password=db_password, db_port=db_port)
        return postgres_connection

    def main(self):
        connection = self.get_postgres_connection()
        zabbix_host_name_setter = ZabbixHostNameSetter(connection=connection)
        print("=" * 100)
        print("Starting zabbix host name setter")
        print("Developed by: AHMED ELKHAYYAT")
        print("Email: elkhayyat.me@gmail.com")
        print("Github: https://github.com/elkhayyat")
        print("Linkedin: https://www.linkedin.com/in/elkhayyat/")
        print("Website: https://elkhayyat.me")
        print("=" * 100)
        print("1. Set host name to system name for all hosts")
        print("2. Set host name to system name for certain host")
        print("3. Exit")
        print("Choose action:")
        action = input()
        if action == "1":
            zabbix_host_name_setter.run()
        elif action == "2":
            print("Enter host id:")
            host_id = input()
            zabbix_host_name_setter.run_for_certain_host_id(host_id)
        elif action == "3":
            exit(0)
        else:
            print("Wrong action")
            exit(1)


Main().main()
