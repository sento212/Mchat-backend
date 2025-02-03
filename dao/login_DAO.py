from settings.DAO_builder import Dao_builder
import hashlib

def login_data(name, Pass,acess_token):
    Sqlbuilder = Dao_builder(['Mchat'])
    CheckConn = Sqlbuilder.ConnTest()
    if(CheckConn['status'] == 200):
        data = bytes(Pass, 'utf-8')
        md5_hash = hashlib.md5(data)
        Pass = md5_hash.hexdigest()
        query = """select username, TO_CHAR(entry_date, 'YYYY-MM-DD HH24:MI:SS') entry from userdata where username = %(username)s and password = %(password)s""" 
        params = {'username': name, 'password' : Pass}
        hasil = Sqlbuilder.Select('Mchat', query, params)
        if not hasil['data']:
            return {'status' : 400, 'message' : 'user tidak ada silahkan dicoba lagi'}
        if(hasil['status'] == 400):
            return {'status' : 400, 'message' : hasil['message']}
        hasil["key_token"] = acess_token
        return hasil
    
    else:
        raise Exception(CheckConn)