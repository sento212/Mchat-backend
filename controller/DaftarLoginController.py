from dao.daftar_DAO import daftar_login
from flask import request
import traceback

class daftarloginController:

    def PUT(self, *args, **kwargs):
        try:
            name = request.form.get('user',None)
            Pass = request.form.get('pass',None)
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