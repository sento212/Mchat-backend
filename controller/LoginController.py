from dao.login_DAO import login_data
from flask import request
import traceback
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from settings.caches import save_to_file, load_from_file

class loginController:

    def POST(self, *args, **kwargs):
        try:
            caches = load_from_file("list_token")
            name = request.form.get('user',None)
            Pass = request.form.get('pass',None)
            acess_token = create_access_token(identity={'user' : name, 'login_status' : True})
            hasil = login_data(name,Pass,acess_token)
            if(hasil['status'] == 400):
                raise Exception(hasil['message'])
            if(caches != None):
                caches.append(hasil['key_token'])
                list_caches = caches
            else:
                list_caches = []
                list_caches.append(hasil['key_token'])
            save_to_file('list_token', list_caches)
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
    
    @jwt_required()
    def DELETE(self, *args, **kwargs):
        try:
            current_user = get_jwt_identity()
            token = request.headers.get('Authorization')
            token = token[7:]  
            caches = load_from_file("list_token")
            
            if(caches.index(token)):
                index = caches.index(token)
                caches.pop(index)
                save_to_file('list_token', caches)
                return {
                    'status' : 200,
                    'message' : "Logout berhasil" ,
                    } 

        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            error_line = tb[-1].lineno
            file_name = tb[-1].filename
            print(f"{e} on line {error_line} at {file_name}")
            return {
                'status' : 400,
                'message' : "Gagal Logout" 
                } 