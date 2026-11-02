from settings.conn import Conn
import inspect
import asyncio
import re
import json


class Dao_builder:

    def __init__(self): 
        self.Conn = {}
        self.cheking = {}

    async def close_conn(self):
        for key , value  in self.Conn.items():
            await value.close()


    async def get_conn(self, connection_list):
        Chatconn = Conn('localhost','sento','cfu800212345','mchat', '5555')
        if 'Mchat' in connection_list:
            hasil = await Chatconn.get_conn()
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

        return self.cheking


    def ConnTest(self):
        return self.cheking
    
    async def Select(self, Conn, querry, param = None):
        try:
            if Conn in self.Conn:
                cur = self.Conn[Conn]
                if isinstance(param, dict): 

                    keys = re.findall(r'%\((.*?)\)s', querry)
                    
                    # Replace %(key)s with asyncpg's $1, $2, $3...
                    for index, key in enumerate(keys, start=1):
                        querry = querry.replace(f"%({key})s", f"${index}", 1)
                    
                    # Extract values in the exact order they appear in the query
                    values = tuple(param[key] for key in keys)
                    rows = await cur.fetch(querry, *values)
                elif isinstance(param, (list, tuple)):
                    counter = 1
                    while '%s' in querry:
                        querry = querry.replace('%s', f'${counter}', 1)
                        counter += 1
                    rows = await cur.fetch(querry, *param)
                else:
                    rows = await cur.fetch(querry)

                hasil = [dict(row) for row in rows]
                print(hasil)
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
        
    async def ExecuteCommit(self, Conn, querry, param):
        try:
            if Conn in self.Conn:
                cur = self.Conn[Conn]
                if isinstance(param, dict): 

                    keys = re.findall(r'%\((.*?)\)s', querry)
                    
                    # Replace %(key)s with asyncpg's $1, $2, $3...
                    for index, key in enumerate(keys, start=1):
                        querry = querry.replace(f"%({key})s", f"${index}", 1)
                    
                    # Extract values in the exact order they appear in the querry
                    values = tuple(param[key] for key in keys)
                    await cur.fetchrow(querry, *values)

                elif isinstance(param, (list, tuple)):
                                    counter = 1
                                    while '%s' in querry:
                                        querry = querry.replace('%s', f'${counter}', 1)
                                        counter += 1
                                    rows = await cur.fetchrow(querry, *param)
                else:
                    await cur.fetchrow(querry)
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
                                        
    async def Rollback(self, Conn):
        try:
            if Conn in self.Conn:
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







        