from flask import Flask, request
from flask_cors import CORS
import threading, asyncio, websockets, os , json
from index import routing
from settings.authentication import Authentication
from flask_caching import Cache
from settings.caches import save_to_file, load_from_file
from urllib.parse import urlparse, parse_qs

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

async def handler(websocket, path):
    try:
        parts = path.split("?")
        new_path = parts[0].replace("/", "")

        parsed_url = urlparse(path)
        params = parse_qs(parsed_url.query)
        token = params.get('Authorization', 400)[0]
        caches = load_from_file("list_token")
        if(caches.index(token)):      
            hasil = await routing.Run_websockets(path = new_path,route = 'WSC', websocket = websocket, rawroute = path)
            return hasil
    except Exception as e:
        hasil_check = {
            'status' : 401,
            'message' : "Token Expired" ,
            } 
        print(hasil_check)
        await websocket.send(json.dumps(hasil_check, default=str)) 

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


async def main():
    # async with websockets.serve(handler, "localhost", 8765, ping_interval=20, ping_timeout=10):
    #     await asyncio.Future() 
    server =  await websockets.serve(handler, "localhost", 8765, ping_interval=20, ping_timeout=10)
    try:
        await server.wait_closed()
    except asyncio.CancelledError:
        print("Server is shutting down...")
        server.close()
        os._exit(0)
        # await server.wait_closed()

    
if __name__ == '__main__':
    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()
    asyncio.run(main())