from settings.DAO_builder import Dao_builder
import json, sys, asyncio
import functools

async def add_chat(main_user,conv_id,chat):
    Sqlbuilder = Dao_builder()
    CheckConn = await Sqlbuilder.get_conn(['Mchat'])
    if(CheckConn['status'] == 200):
        query = """SELECT COUNT(1) jml from conversation WHERE (NAME = %(user)s or name_enemy = %(user)s) 
                AND conversation_id = %(id)s  """ 
        params = {'user': main_user,'id': conv_id}
        hasil_check = await Sqlbuilder.Select('Mchat', query, params)
        if(hasil_check['status'] == 400):
            
            raise Exception(hasil_check['message'])
        if(hasil_check['data'][0]['jml'] != 0):

            query = """Insert into chat(conversation_id,username,chat_inside) 
                        values (%(id)s,%(user)s,%(chat)s)""" 
            params = {'id': conv_id,'user': main_user, 'chat' : chat}
            hasil = await Sqlbuilder.ExecuteCommit('Mchat', query, params)
            if(hasil['status'] == 400):
                
                return{
                    'status' : 400,
                    'message' : "Gagal mendapatkan data" 
                    } 
            return hasil
        else:
            return{
                'status' : 400,
                'message' : "akun tidak ada!!!"}
    else:
        raise Exception(CheckConn)

async def show_save(websocket,conv_id,user):
    try:
        Sqlbuilder = Dao_builder()
        CheckConn = await Sqlbuilder.get_conn(['Mchat'])
        if(CheckConn['status'] == 200):
            query = """SELECT COUNT(1) jml from conversation WHERE (NAME = %(user)s or name_enemy = %(user)s) 
                    AND conversation_id = %(id)s  """ 
            params = {'user': user,'id': conv_id}
            hasil_check = await Sqlbuilder.Select('Mchat', query, params)
            if(hasil_check['status'] == 400):
                await Sqlbuilder.Rollback('Mchat') 
                await websocket.send(json.dumps(hasil_check, default=str))       
            if(hasil_check['data'][0]['jml'] != 0):
                while True:
                    message = await websocket.recv()
                    message = json.loads(message)
                    if(message['tipe'] == 'put'):
                            chat = message['chat']
                            if chat != '':
                                query = """Insert into chat(conversation_id,username,chat_inside) 
                                            values (%(id)s,%(user)s,%(chat)s)""" 
                                params = {'id': conv_id,'user': user, 'chat' : chat}
                                hasil = await Sqlbuilder.ExecuteCommit('Mchat', query, params) 
                                if(hasil['status'] == 400):
                                    await Sqlbuilder.Rollback('Mchat') 
                                    await websocket.send(json.dumps(hasil, default=str))
                    else:
                        hasil_check = {'status' : 400, 'message' : "tipe tidak ada"}
                        await websocket.send(json.dumps(hasil_check, default=str))   
            else:
                hasil_check = {'status' : 400, 'message' : "akun tidak ada!!!"}
                await websocket.send(json.dumps(hasil_check, default=str)) 
        else:
            await websocket.send(json.dumps(CheckConn, default=str)) 
            raise Exception(CheckConn)
    except Exception as e:
        await Sqlbuilder.Rollback('Mchat')
        current_module_file = sys.modules[__name__].__file__
        exc_type, exc_value, exc_traceback = sys.exc_info()
        line = sys.exc_info()[-1].tb_lineno
        print(f"Websocket error {exc_value} {exc_type} on {current_module_file} at line {line}")

async def show_chat(connection, pid, channel, payload, conv_id, websocket, Sqlbuilder):
    data = json.loads(payload)
    query = """select a.chat_inside, a.username, TO_CHAR(a.entry_date, 'HH24-MI') entry_date from chat a where conversation_id = %(id)s
                order by a.id asc""" 
    params = {'id': conv_id}
    hasil_check = await Sqlbuilder.Select('Mchat', query, params)
    await websocket.send(json.dumps(hasil_check, default=str))  
    

async def list_chat( websocket,conv_id,user):
        
        Sqlbuilder = Dao_builder()
        CheckConn = await Sqlbuilder.get_conn(['Mchat'])
        if(CheckConn['status'] == 200):
            query = """SELECT COUNT(1) jml from conversation WHERE (NAME = %(user)s or name_enemy = %(user)s) 
                    AND conversation_id = %(id)s  """ 
            params = {'user': user,'id': conv_id}
            hasil_check = await Sqlbuilder.Select('Mchat', query, params)
            if(hasil_check['status'] == 400):
                await Sqlbuilder.Rollback('Mchat')
                raise Exception(hasil_check['message'])
            if(hasil_check['data'][0]['jml'] != 0):
                    query = """select a.chat_inside, a.username, TO_CHAR(a.entry_date, 'HH24-MI') entry_date from chat a where conversation_id = %(id)s
                                order by a.id asc""" 
                    params = {'id': conv_id}
                    hasil_check = await Sqlbuilder.Select('Mchat', query, params)
                    await websocket.send(json.dumps(hasil_check, default=str))  

                    bound_callback = functools.partial(show_chat, conv_id = conv_id, websocket = websocket, Sqlbuilder = Sqlbuilder)
                    
                    await Sqlbuilder.Conn['Mchat'].add_listener(f"chat_channel_{conv_id}", bound_callback)

                    while True:
                        await asyncio.sleep(3600)

            else:
                hasil_check = {'status' : 400, 'message' : "akun tidak ada"}
                await websocket.send(json.dumps(hasil_check, default=str)) 
        else:
            await Sqlbuilder.Rollback('Mchat')
            current_module_file = sys.modules[__name__].__file__
            exc_type, exc_value, exc_traceback = sys.exc_info()
            line = sys.exc_info()[-1].tb_lineno
            print(f"Websocket error {exc_value} {exc_type} on {current_module_file} at line {line}")
            

                
