from settings.DAO_builder import Dao_builder
from datetime import datetime
import json
import sys
from datetime import timedelta
# import asyncio

websocket_list = []

def show_temen(name, cari):
    Sqlbuilder = Dao_builder(['Mchat'])
    CheckConn = Sqlbuilder.ConnTest()
    if(CheckConn['status'] == 200):
        if(cari != ''):
            query = """SELECT username from userdata WHERE username NOT IN 
                    (select name_enemy from conversation where NAME = %(username)s or name_enemy = %(username)s)
                    AND username LIKE %(cari)s""" 
            params = {'username': name, 'cari': cari+'%'}
            hasil_check = Sqlbuilder.Select('Mchat', query, params)
            if(hasil_check['status'] == 400):
                Sqlbuilder.Rollback('Mchat')
            return hasil_check
        else:
            return{
                'status' : 200,
                'message' : "data kosong",
                'data' : []}
    else:
        raise Exception(CheckConn)

def daftar_temen(name,nama_temen):
    Sqlbuilder = Dao_builder(['Mchat'])
    CheckConn = Sqlbuilder.ConnTest()
    if(CheckConn['status'] == 200):
        query = """select count(name_enemy) jml from conversation where name = %(username)s and name_enemy =%(userenemy)s  """ 
        params = {'username': name,'userenemy': nama_temen}
        hasil_check = Sqlbuilder.Select('Mchat', query, params)
        if(hasil_check['status'] == 400):
            Sqlbuilder.Rollback('Mchat')
            raise Exception(hasil_check['message'])

        if(hasil_check['data'][0]['jml'] == 0):
            hasil_check = Sqlbuilder.Select('Mchat', query, params)
            convid = "comvid_"+str(datetime.now())
            query = """Insert into Conversation(name,name_enemy,conversation_id) 
                        values (%(name)s,%(name_enemy)s,%(convid)s)""" 
            params = {'name': name,'name_enemy': nama_temen, 'convid' : convid}
            hasil = Sqlbuilder.ExecuteCommit('Mchat', query, params)
            if(hasil['status'] == 400):
                Sqlbuilder.Rollback('Mchat')
                raise Exception(hasil['message'])
            return hasil
        else:
            return{
                'status' : 400,
                'message' : "akun sudah berteman!!!"}
    else:
        raise Exception(CheckConn)

async def shoot(user,conv_id):
    try:
        Sqlbuilder = Dao_builder(['Mchat'])
        CheckConn = Sqlbuilder.ConnTest()
        if(CheckConn['status'] == 200):
            query = """SELECT name, name_enemy from conversation WHERE conversation_id = %(id)s  """ 
            params = {'user': user,'id': conv_id}
            hasil_check = await Sqlbuilder.AsyncronusCall('Select','Mchat', query, params)
            list_me = []
            if hasil_check["data"][0]["name"] == hasil_check["data"][0]["name_enemy"]:
                list_me.append(hasil_check["data"][0]["name"])
            else:
                list_me.append(hasil_check["data"][0]["name"])
                list_me.append(hasil_check["data"][0]["name_enemy"])
            for list in websocket_list:
                if list["user"] in list_me:
                    websocket = list["web"]
                    user = list["user"]
                    query = """SELECT ion.conversation_id, case when ion.name_enemy = %(username)s THEN ion.name ELSE ion.name_enemy END AS name_enemy, ca.chat_inside, TO_CHAR(ca.entry_date, 'HH24-MI') entry_date
                                    from conversation ion  left JOIN chat ca
                                    ON ion.conversation_id = ca.conversation_id
                                    WHERE (ca.entry_date = (
                                    SELECT MAX(cab.entry_date) from chat cab 
                                    where cab.conversation_id = ion.conversation_id
                                    )
                                    OR ca.entry_date IS null)
                                    and (ion.NAME = %(username)s or ion.name_enemy = %(username)s)
                                    order BY CASE WHEN  ca.entry_date IS not NULL THEN ca.entry_date 
												ELSE ion.entry_date end desc""" 
                    params = {'username': user}
                    hasil_check = await Sqlbuilder.AsyncronusCall('Select','Mchat', query, params)
                    if(hasil_check['status'] == 400):
                        Sqlbuilder.Rollback('Mchat')
                    await websocket.send(json.dumps(hasil_check, default=str))   
    except Exception as e:
        Sqlbuilder.Rollback('Mchat')
        current_module_file = sys.modules[__name__].__file__
        exc_type, exc_value, exc_traceback = sys.exc_info()
        line = sys.exc_info()[-1].tb_lineno
        print(f"Websocket error {exc_value} {exc_type} on {current_module_file} at line {line}")  

async def addshow(websocket,user):
    try:
        Sqlbuilder = Dao_builder(['Mchat'])
        CheckConn = Sqlbuilder.ConnTest()
        if(CheckConn['status'] == 200):
            while True:
                message = await websocket.recv()
                message = json.loads(message)
                print(message)
                if(message['tipe'] == 'put'):
                    nama_temen = message['nama_temen']
                    query = """select count(name_enemy) jml from conversation where name = %(username)s and name_enemy =%(userenemy)s  """ 
                    params = {'username': user,'userenemy': nama_temen}
                    hasil_check = await Sqlbuilder.AsyncronusCall('Select','Mchat', query, params)
                    if(hasil_check['status'] == 400):
                        Sqlbuilder.Rollback('Mchat')

                    if(hasil_check['data'][0]['jml'] == 0):
                        hasil_check = Sqlbuilder.Select('Mchat', query, params)
                        convid = "comvid_"+str(datetime.now())
                        query = """Insert into Conversation(name,name_enemy,conversation_id) 
                                    values (%(name)s,%(name_enemy)s,%(convid)s)""" 
                        params = {'name': user,'name_enemy': nama_temen, 'convid' : convid}
                        hasil = await Sqlbuilder.AsyncronusCall('ExecuteCommit','Mchat', query, params)
                        if(hasil['status'] == 400):
                            Sqlbuilder.Rollback('Mchat')
                    else:
                        hasil_check = {'status' : 400, 'message' : "akun sudah berteman!!!"}
                        await websocket.send(json.dumps(hasil_check, default=str))  
                elif(message['tipe'] == 'get'):
                    query = """SELECT ion.conversation_id, case when ion.name_enemy = %(username)s THEN ion.name ELSE ion.name_enemy END AS name_enemy, ca.chat_inside, TO_CHAR(ca.entry_date, 'HH24-MI') entry_date
                                    from conversation ion  left JOIN chat ca
                                    ON ion.conversation_id = ca.conversation_id
                                    WHERE (ca.entry_date = (
                                    SELECT MAX(cab.entry_date) from chat cab 
                                    where cab.conversation_id = ion.conversation_id
                                    )
                                    OR ca.entry_date IS null)
                                    and (ion.NAME = %(username)s or ion.name_enemy = %(username)s)
                                    order BY CASE WHEN  ca.entry_date IS not NULL THEN ca.entry_date 
												ELSE ion.entry_date end desc""" 
                    params = {'username': user}
                    hasil_check = await Sqlbuilder.AsyncronusCall('Select','Mchat', query, params)
                    if(hasil_check['status'] == 400):
                        Sqlbuilder.Rollback('Mchat')
                    await websocket.send(json.dumps(hasil_check, default=str))     
                
                else:
                    hasil_check = {'status' : 400, 'message' : "tipe tidak ada"}
                    await websocket.send(json.dumps(hasil_check, default=str)) 
        else:
            await websocket.send(json.dumps(CheckConn, default=str)) 
            raise Exception(CheckConn)
    except Exception as e:
        Sqlbuilder.Rollback('Mchat')
        current_module_file = sys.modules[__name__].__file__
        exc_type, exc_value, exc_traceback = sys.exc_info()
        line = sys.exc_info()[-1].tb_lineno
        print(f"Websocket error {exc_value} {exc_type} on {current_module_file} at line {line}")

async def dafter_temen(websocket,user):
    try:
        banyak = 0
        Sqlbuilder = Dao_builder(['Mchat'])
        CheckConn = Sqlbuilder.ConnTest()
        if(CheckConn['status'] == 200):
            while True:
                    query = """SELECT COUNT(1) from conversation where NAME = %(username)s or name_enemy = %(username)s""" 
                    params = {'username': user}
                    hasil_check = await Sqlbuilder.AsyncronusCall('Select','Mchat', query, params)
                    if(hasil_check['status'] == 400):
                        Sqlbuilder.Rollback('Mchat')
                    if(hasil_check['data'][0] != banyak):
                        banyak = hasil_check['data'][0]
                        query = """SELECT ion.conversation_id, case when ion.name_enemy = %(username)s THEN ion.name ELSE ion.name_enemy END AS name_enemy, ca.chat_inside, TO_CHAR(ca.entry_date, 'HH24-MI') entry_date
                                    from conversation ion  left JOIN chat ca
                                    ON ion.conversation_id = ca.conversation_id
                                    WHERE (ca.entry_date = (
                                    SELECT MAX(cab.entry_date) from chat cab 
                                    where cab.conversation_id = ion.conversation_id
                                    )
                                    OR ca.entry_date IS null)
                                    and (ion.NAME = %(username)s or ion.name_enemy = %(username)s)
                                    order BY CASE WHEN  ca.entry_date IS not NULL THEN ca.entry_date 
												ELSE ion.entry_date end desc""" 
                        params = {'username': user}
                        hasil_check = await Sqlbuilder.AsyncronusCall('Select','Mchat', query, params)
                        if(hasil_check['status'] == 400):
                            Sqlbuilder.Rollback('Mchat')
                        # identity = str(id(websocket))
                        chek = 0
                        for list in websocket_list:
                            if list["user"] == user and list["web"] != websocket:
                                list.update({"web": websocket })
                                chek = 1
                        if(chek == 0):
                            websocket_list.append({ "user" : user, "web": websocket })
                        await websocket.send(json.dumps(hasil_check, default=str))           
                    # await asyncio.sleep(5)
        else:
            await websocket.send(json.dumps(CheckConn, default=str)) 
            raise Exception(CheckConn)
    except Exception as e:
        Sqlbuilder.Rollback('Mchat')
        current_module_file = sys.modules[__name__].__file__
        exc_type, exc_value, exc_traceback = sys.exc_info()
        line = sys.exc_info()[-1].tb_lineno
        print(f"Websocket error {exc_value} {exc_type} on {current_module_file} at line {line}")


