class ZabbixHostNameSetter:
    def __init__(self, connection):
        self.connection = connection

    def get_hosts(self):
        self.connection.connect()
        self.connection.cursor.execute("SELECT hostid, host FROM hosts")
        return self.connection.cursor.fetchall()

    def get_host_by_host_id(self, host_id):
        self.connection.connect()
        self.connection.cursor.execute("SELECT hostid, host FROM hosts WHERE hostid = %s" % host_id)
        return self.connection.cursor.fetchone()

    def get_host_system_name_item_id(self, host_id):
        self.connection.connect()
        self.connection.cursor.execute("SELECT itemid FROM items WHERE hostid = %s AND name = 'System name'" % host_id)
        return self.connection.cursor.fetchone()

    def get_host_system_name(self, item_id):
        self.connection.connect()
        self.connection.cursor.execute(
            "SELECT value FROM history_str WHERE itemid = %s ORDER BY clock DESC LIMIT 1" % item_id)
        return self.connection.cursor.fetchone()

    def set_host_name_to_host_system_name(self, host_id, host_name):
        self.connection.connect()
        self.connection.cursor.execute("UPDATE hosts SET name = '%s' WHERE hostid = %s" % (host_name, host_id))
        self.connection.connection.commit()

    def get_host_name_for_host_id(self, host_id):
        self.connection.connect()
        self.connection.cursor.execute("SELECT name FROM hosts WHERE hostid = %s" % host_id)
        return self.connection.cursor.fetchone()

    def run(self):
        hosts = self.get_hosts()
        for host in hosts:
            host_id = host[0]
            self.run_for_certain_host_id(host_id)

    def run_for_certain_host_id(self, host_id):
        host = self.get_host_by_host_id(host_id)
        host_name = host[1]
        item_id = self.get_host_system_name_item_id(host_id)
        if item_id:
            item_id = item_id[0]
            print(f"1. Host name: {host_name}")
            print(f"2. Item id: {item_id}")
            host_system_name = self.get_host_system_name(item_id)
            print(f"3.0 Host system name: {host_system_name}")
            if host_system_name:
                host_system_name = host_system_name[0]
                print(f"3.1 Host system name: {host_system_name}")
                if host_system_name != host_name:
                    self.set_host_name_to_host_system_name(host_id, host_system_name)
                    print('Host %s name changed to %s' % (host_name, host_system_name))
                    new_host_name = self.get_host_name_for_host_id(host_id)
                    print(f"4. New host name: {new_host_name}")
                else:
                    print('Host %s name is already %s' % (host_name, host_system_name))
            else:
                print('Host %s has no system name' % host_name)
        else:
            print('Host %s has no system name item' % host_name)
