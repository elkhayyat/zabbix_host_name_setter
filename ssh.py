import os

import paramiko
from dotenv import load_dotenv

load_dotenv()


class SSHConnection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, self.port, self.username, self.password)

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdin, stdout, stderr

    def close(self):
        self.client.close()


host = os.getenv('SSH_HOST')
port = os.getenv('SSH_PORT')
username = os.getenv('SSH_USER')
password = os.getenv('SSH_PASS')

ssh_connection = SSHConnection(host=host, port=port, username=username, password=password)
ssh_connection.connect()
stdin, stdout, stderr = ssh_connection.execute_command('python3 /root/zabbix_host_name_setter/main.py')
