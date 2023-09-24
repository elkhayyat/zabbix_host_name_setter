import psycopg2


class PostgresConnection:
    def __init__(self, db_host, db_name, db_user, db_password, db_port):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.db_host,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            port=self.db_port
        )
        self.cursor = self.connection.cursor()
