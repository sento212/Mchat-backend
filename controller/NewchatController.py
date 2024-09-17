from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from dao.new_chat_DAO import add_chat, list_chat, show_save
import jwt, asyncio, sys, traceback
from urllib.parse import urlparse, parse_qs

class newchatController:

    @jwt_required()
    def PUT(self, *args, **kwargs):
        try:
            current_user = get_jwt_identity()
            main_user = current_user['user']
            chat = request.form.get('chat',None)
            conv_id = request.form.get('conversation_id',None)
            hasil = add_chat(main_user,conv_id,chat)
            if(hasil['status'] == 400):
                return hasil
            return hasil
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            error_line = tb[-1].lineno
            file_name = tb[-1].filename
            print(f"{e} on line {error_line} at {file_name}")
            return {
                'status' : 400,
                'message' : "Gagal mendapatkan data" 
                } 
        
    async def WSC(self, websocket, path):
        try:
            parsed_url = urlparse(path)
            params = parse_qs(parsed_url.query)
            token = params.get('Authorization', 400)[0]
            conversation_id = params.get('conversation_id', 400)[0]
            payload = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
            user = payload['sub']['user']
            await asyncio.gather(
                show_save(websocket,conversation_id,user),
                list_chat(websocket,conversation_id,user)
            )
        except Exception as e:
            current_module_file = sys.modules[__name__].__file__
            exc_type, exc_value, exc_traceback = sys.exc_info()
            line = sys.exc_info()[-1].tb_lineno
            print(f"Websocket error {exc_type} on {current_module_file} at line {line}, {exc_value}")