import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class PostgresConnection:
    def __init__(self, use_ssh_tunnel=False):
        self.connection = None
        self.cursor = None
        self.use_ssh_tunnel = use_ssh_tunnel

    def connect(self):
        self.connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            port=os.getenv('DB_PORT')
        )
        self.cursor = self.connection.cursor()
