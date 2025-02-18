from urllib.parse import urlparse, parse_qs
from index import routing
import threading, asyncio, websockets, os , json, requests, signal
from websockets import serve

async def handler(websocket, path):
    try:
        parts = path.split("?")
        new_path = parts[0].replace("/", "")

        parsed_url = urlparse(path)
        params = parse_qs(parsed_url.query)
        token = params.get('Authorization', 400)[0]
        url = "https://sento.my.id/sento/backend/DaftarLogin"
        payload = {'token': token}
        response = requests.request("POST", url, data=payload)
        if(json.loads(response.text)['status'] == 200): 
            hasil = await routing.Run_websockets(path = new_path,route = 'WSC', websocket = websocket, rawroute = path)
            return hasil
        else:
            raise Exception(response.text)
    except Exception as e:
        hasil_check = {
            'status' : 401,
            'message' : "Token Expired",
            } 
        await websocket.send(json.dumps(hasil_check, default=str)) 

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with serve(
        handler,
        host="localhost",
        port=8000 + int(os.environ["SUPERVISOR_PROCESS_NAME"][-2:]),
        reuse_port=True,
    ):
        await stop

# async def main():
#     # async with websockets.serve(handler, "localhost", 8765, ping_interval=20, ping_timeout=10):
#     #     await asyncio.Future() 
#     server =  await websockets.serve(handler, "0.0.0.0", 8000, ping_interval=20, ping_timeout=10)
#     # loop = asyncio.get_running_loop()
#     # stop = loop.create_future()
#     # loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

#     # async with unix_serve(
#     #     handler,
#     #     path=f"proxy/{os.environ['SUPERVISOR_PROCESS_NAME']}.sock",
#     # ):
#     #     await stop
#     try:
#         print("Server is running...")
#         await server.wait_closed()
#     except asyncio.CancelledError:
#         print("Server is shutting down...")
#         server.close()
#         os._exit(0)
#         await server.wait_closed()
        

if __name__ == '__main__':
    asyncio.run(main())
    # main()
