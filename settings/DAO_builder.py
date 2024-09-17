from settings.conn import Conn
import inspect
import asyncio


class Dao_builder:

    def __init__(self,connection_list):
        Chatconn = Conn('localhost','postgres','800212','Mchat', '5432')
        self.Conn = {}
        if 'Mchat' in connection_list:
            hasil = Chatconn.get_conn()
            if hasil['status'] == 200:
                self.Conn['Mchat'] = hasil['data']
            else:
                self.cheking = hasil
        if len(self.Conn) != len(connection_list):
            self.cheking = {
                'status' : 400,
                'message' : 'Failed to establish connection'
            }
        else:
            self.cheking = {
                'status' : 200,
                'message' : 'Connection sacure'
            }

    def ConnTest(self):
        return self.cheking
    
    def Select(self, Conn, querry, param):
        try:
            if Conn in self.Conn:
                cur = self.Conn[Conn].cursor()
                cur.execute(querry, param)
                data = cur.fetchall()
                hasil = []
                for coldata in data:
                    hasil.append({col[0] : coldata[key] for key, col in enumerate(cur.description)})

                return {
                    'status' : 200,
                    'message' : 'Select data berhasil',
                    'data' : hasil
                }
            else:
                raise Exception("No Connection detected")
        except Exception as e:
            caller_frame = inspect.stack()[1]
            print(f"you have error in you sql syntax {e} on {caller_frame.filename} at line {caller_frame.lineno}")    
            return {
            'status' : 400,
            'message' : 'An Error Accured'
            } 
        
    def ExecuteCommit(self, Conn, querry, param):
        try:
            if Conn in self.Conn:
                cur = self.Conn[Conn].cursor()
                cur.execute(querry, param)
                self.Conn[Conn].commit()
                return {
                    'status' : 200,
                    'message' : 'Execute data berhasil'
                }
            else:
                raise Exception("No Connection detected")
        except Exception as e:
            caller_frame = inspect.stack()[1]
            print(f"you have error in you sql syntax {e} on {caller_frame.filename} at line {caller_frame.lineno}")
            return {
                'status' : 400,
                'message' : 'An Error Accured'
                } 
                                 
    def ExecuteNoCommit(self, Conn, querry, param):
        try:
            if Conn in self.Conn:
                cur = self.Conn[Conn].cursor()
                cur.execute(querry, param)
                return {
                    'status' : 200,
                    'message' : 'Execute data berhasil'
                }
            else:
                raise Exception("No Connection detected")
        except Exception as e:
            caller_frame = inspect.stack()[1]
            print(f"you have error in you sql syntax {e} on {caller_frame.filename} at line {caller_frame.lineno}")  
            return {
            'status' : 400,
            'message' : 'An Error Accured'
            } 
        
    def Commit(self, Conn):
        try:
            if Conn in self.Conn:
                self.Conn[Conn].commit()
                return {
                    'status' : 200,
                    'message' : 'Execute data berhasil'
                }
            else:
                raise Exception("No Connection detected") 
        except Exception as e:
            print(e)  
            return {
            'status' : 400,
            'message' : 'An Error Accured'
            }  
    
    def Rollback(self, Conn):
        try:
            if Conn in self.Conn:
                self.Conn[Conn].rollback()
                return {
                    'status' : 200,
                    'message' : 'Execute data berhasil'
                }
            else:
                raise Exception("No Connection detected") 
        except Exception as e:
            print(e)  
            return {
            'status' : 400,
            'message' : 'An Error Accured'
            }  

    async def AsyncronusCall(self,tipe,database,querry,param):
        try:
            caller_frame = inspect.stack()[1]
            if hasattr(Dao_builder, tipe):
                calling = getattr(self, tipe)
                hasil =  await asyncio.to_thread(calling,database, querry, param)
                if hasil == 400:
                    raise Exception("No Connection detected") 
                return hasil
            else:
                raise Exception(f"No action name {tipe} in builder")
        except Exception as e:
            print(e)
            caller_frame = inspect.stack()[1]
            print(f"you have error in you sql syntax {e} on {caller_frame.filename} at line {caller_frame.lineno}")    
            return {
            'status' : 400,
            'message' : 'An Error Accured'
            } 

        