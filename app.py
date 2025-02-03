from flask import Flask, request
from flask_cors import CORS
import asyncio
from index import routing
from settings.authentication import Authentication
from flask_caching import Cache
from settings.caches import save_to_file, load_from_file


config = {
    "debug": True,          
    'use_reloader': False,
    "CACHE_TYPE": "SimpleCache"
}
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(config)
    return app

app = create_app()
CORS(app)
Authentication(app)
cache = Cache(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET','POST','DELETE','PUT'])
# @cache.cached(timeout=None)
def run(path):
    try:
        token = request.headers.get('Authorization', None)
        if token != None:
            caches = load_from_file("list_token")
            token = token[7:]  
            if(caches.index(token)):      
                hasil = routing.Run(path = path,route = request.method, cache = cache)
                return hasil
        else:
            hasil = routing.Run(path = path,route = request.method, cache = cache)
            return hasil
    except Exception as e:
        return {
                'status' : 400,
                'message' : "Token Expired" ,
                } 

    
if __name__ == '__main__':
    # flask_thread = threading.Thread(target=app.run)
    # flask_thread.start()
    # asyncio.run(main())
    app.run(debug=True, host='0.0.0.0')