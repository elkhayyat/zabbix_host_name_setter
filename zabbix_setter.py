class ZabbixHostNameSetter:
    def __init__(self, connection):
        self.connection = connection
        self.count = 0
        self.summary_counter = {
            "total": 0,
            "changed": 0,
            "already_has_system_name": 0,
            "has_no_system_name": 0,
            "has_no_system_name_item": 0
        }

    def get_hosts(self):
        self.connection.connect()
        self.connection.cursor.execute("SELECT hostid, name FROM hosts")
        return self.connection.cursor.fetchall()

    def get_host_by_host_id(self, host_id):
        self.connection.connect()
        self.connection.cursor.execute("SELECT hostid, name FROM hosts WHERE hostid = %s" % host_id)
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

    def run(self):
        hosts = self.get_hosts()
        for host in hosts:
            self.count += 1
            host_id = host[0]
            self.run_for_certain_host_id(host_id)
        self.summary_counter["total"] = self.count
        self.print_summary_report()

    def run_for_certain_host_id(self, host_id):
        host = self.get_host_by_host_id(host_id)
        host_name = host[1]
        item_id = self.get_host_system_name_item_id(host_id)
        if item_id:
            item_id = item_id[0]
            host_system_name = self.get_host_system_name(item_id)
            if host_system_name:
                host_system_name = host_system_name[0]
                if host_system_name != host_name:
                    self.set_host_name_to_host_system_name(host_id, host_system_name)
                    self.summary_counter["changed"] += 1
                    print(f"{self.count}. Host {host_name} name changed to {host_system_name}")
                else:
                    self.summary_counter["already_has_system_name"] += 1
                    print(f"{self.count}. Host {host_name} name is already {host_system_name}")
            else:
                self.summary_counter["has_no_system_name"] += 1
                print(f"{self.count}. Host {host_name} has no system name")
        else:
            self.summary_counter["has_no_system_name_item"] += 1
            print(f"{self.count}. Host {host_name} has no system name item")

    def print_summary_report(self):
        print("=" * 100)
        print("Done")
        print("=" * 100)
        print(f"Total hosts: {self.summary_counter.get('total')}")
        print(f"Changed hosts: {self.summary_counter.get('changed')}")
        print(f"Already has system name hosts: {self.summary_counter.get('already_has_system_name')}")
        print(f"Has no system name hosts: {self.summary_counter.get('has_no_system_name')}")
        print(f"Has no system name item hosts: {self.summary_counter.get('has_no_system_name_item')}")
        print("=" * 100)