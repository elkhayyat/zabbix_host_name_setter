import os

import paramiko
from dotenv import load_dotenv

load_dotenv()


class SSHConnection:
    def __init__(self):
        self.host = os.getenv('SSH_HOST')
        self.port = int(os.getenv('SSH_PORT'))
        self.username = os.getenv('SSH_USER')
        self.password = os.getenv('SSH_PASS')
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdin, stdout, stderr

    def close(self):
        self.client.close()
