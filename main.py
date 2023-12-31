from dotenv import load_dotenv

from postgres import PostgresConnection
from zabbix_setter import ZabbixHostNameSetter

load_dotenv()


class Main:
    @staticmethod
    def index():
        print("=" * 100)
        print("Starting zabbix host name setter")
        print("Developed by: AHMED ELKHAYYAT")
        print("Email: elkhayyat.me@gmail.com")
        print("Github: https://github.com/elkhayyat")
        print("Linkedin: https://www.linkedin.com/in/elkhayyat/")
        print("Website: https://elkhayyat.me")
        print("=" * 100)

    @staticmethod
    def first_page():
        print("=" * 100)
        print("1. Set host name to system name for all hosts")
        print("2. Set host name to system name for certain host")
        print("3. Exit")
        print("Choose action:")

    @staticmethod
    def second_page():
        print("=" * 100)
        print("Note: You can get host id from zabbix web interface")
        print("Enter host id:")

    def main(self):
        connection = PostgresConnection()
        zabbix_host_name_setter = ZabbixHostNameSetter(connection=connection)
        self.index()
        self.first_page()
        action = input()
        if action == "1":
            zabbix_host_name_setter.run()
        elif action == "2":
            self.second_page()
            host_id = input()
            zabbix_host_name_setter.run_for_certain_host_id(host_id)
        elif action == "3":
            exit(0)
        else:
            print("Wrong action")
            exit(1)


Main().main()
