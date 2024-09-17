from settings.DAO_builder import Dao_builder
import hashlib

def daftar_login(name,Pass):
    Sqlbuilder = Dao_builder(['Mchat'])
    CheckConn = Sqlbuilder.ConnTest()
    if(CheckConn['status'] == 200):
        query = """select count(username) jml from userdata where username = %(username)s """ 
        params = {'username': name}
        hasil_check = Sqlbuilder.Select('Mchat', query, params)
        if(hasil_check['status'] == 400):
            Sqlbuilder.Rollback('Mchat')
            raise Exception(hasil_check['message'])


        if(hasil_check['data'][0]['jml'] == 0):
            data = bytes(Pass, 'utf-8')
            md5_hash = hashlib.md5(data)
            Pass = md5_hash.hexdigest()
            query = """Insert into userdata(username,password) 
                        values (%(username)s,%(password)s)""" 
            params = {'username': name,'password': Pass}
            hasil = Sqlbuilder.ExecuteCommit('Mchat', query, params)
            if(hasil['status'] == 400):
                Sqlbuilder.Rollback('Mchat')
                raise Exception(hasil['message'])
            return hasil
        else:
            return{
                'status' : 400,
                'message' : "akun sudah terdaftar!!!"

            }
    
    else:
        raise Exception(CheckConn)