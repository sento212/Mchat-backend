from flask import render_template
import importlib
import asyncio

class Router:

    def __init__(self):
        self.path = {}

    def AddRoute(self, link, modul, object):
        self.path[link] = {'class' : object, 'modul' : modul}

    def Run(self, **kwargs):
        route = kwargs.get('path')
        method = kwargs.get('route')
        cache = kwargs.get('cache')
        if route in self.path:
            obj = self.path[route]['class']
            modul = self.path[route]['modul']
            module = importlib.import_module(modul)  
            if hasattr(module,obj):
                intence = getattr(module,obj)
                if hasattr(intence(),method):
                    request = getattr(intence(),method)
                    return request(cache = cache)
                else:
                    return {
                'status' : 400,
                'message' : "link tidak ada" 
                } 
            else:
                return {
                'status' : 400,
                'message' : "link tidak ada" 
                } 
        else:
            return {
                'status' : 400,
                'message' : "link tidak ada" 
                } 
        
    async def Run_websockets(self, **kwargs):
        try:
            route = kwargs.get('path')
            method = kwargs.get('route')
            realroute = kwargs.get('rawroute')
            if route in self.path:
                obj = self.path[route]['class']
                modul = self.path[route]['modul']
                module = importlib.import_module(modul)  
                if hasattr(module,obj):
                    intence = getattr(module,obj)
                    if hasattr(intence(),method):
                        websocket = kwargs.get('websocket')
                        request = getattr(intence(),method)
                        await request(websocket,realroute)
                    else:
                        raise Exception("No Connection")
                else:
                    raise Exception("No Connection")
            else:
                raise Exception("No Connection")
        except Exception as e:
            print(f"WebSocket error: {e}")
        