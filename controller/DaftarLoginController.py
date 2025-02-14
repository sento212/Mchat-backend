from dao.daftar_DAO import daftar_login
from flask import request
import traceback
from settings.caches import load_from_file

class daftarloginController:

    def POST(self, *args, **kwargs):
        try:
            caches = load_from_file("list_token")
            token = request.form.get('token',None)
            if token in caches:
                return{
                    'status' : 200,
                    'message' : "token aktif"
                    } 
            else:
                return{
                    'status' : 400,
                    'message' : "token expired"
                    } 
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            error_line = tb[-1].lineno
            file_name = tb[-1].filename
            print(f"{e} on line {error_line} at {file_name}")
            return {
                'status' : 400,
                'message' : "Gagal mendapatkan data" 
                } 

    def PUT(self, *args, **kwargs):
        try:
            print(12, 'yeah')
            name = request.form.get('user',None)
            Pass = request.form.get('pass',None)
            if(name is None or Pass is None):
                return {
                    'status' : 400,
                    'message' : "Username atau Password kosong" 
                    } 
            hasil = daftar_login(name,Pass)
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
                'message' : "Gagal request API" 
                } 