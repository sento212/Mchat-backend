import psycopg2
from sshtunnel import SSHTunnelForwarder


class Conn:
    def __init__(self, host, username, password, db_name, port, db_user):

        self.host = host
        self.username = username
        self.password = password
        self.db_name = db_name
        self.port = port
        self.db_user = db_user
        self.port_ssh = self.ssh_run()
        print('qsqsfvwersfgvwaesfc')
        self.hasil = self.get_conn()



    def ssh_run(self):
        if getattr(self.ssh_run, "has_run", False):
            return self.port_ssh
        SSH_PRIVATE_KEY = "./python"
        with SSHTunnelForwarder(
            (self.host, 22),
            ssh_username=self.username,
            ssh_pkey=SSH_PRIVATE_KEY,
            remote_bind_address=('localhost', self.port)
        ) as tunnel:
            print(f"SSH Tunnel established on local port: {tunnel.local_bind_port}")
            self.ssh_run.has_run = True
            print("This line runs only once, even if the function is called 100 times!")
            return tunnel.local_bind_port

    def get_conn(self):
        try:
            
            conn = psycopg2.connect(
            dbname = self.db_name,
            user = self.db_user,
            password = self.password,
            host = 'localhost',
            port = self.port_ssh
            )

            return {
                'status' : 200,
                'message' : 'connection establish',
                'data'  : conn
            }
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return {
                'status' : 400,
                'message' : 'failed to establish connection'
            }

