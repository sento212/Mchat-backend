import psycopg2


class Conn:
    def __init__(self, host, username, password, db_name, port):
        self.host = host
        self.username = username
        self.password = password
        self.db_name = db_name
        self.port = port
        self.hasil = self.get_conn()

    def get_conn(self):
        try:
            conn = psycopg2.connect(
            dbname = self.db_name,
            user = self.username,
            password = self.password,
            host = self.host,
            port = self.port
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
        

