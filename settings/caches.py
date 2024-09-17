import json

# class Caches:
#     def __init__(self,app):
#         self.app = app
#         # self.get = 
#         # cached_data = cache.get('my_Data')
#         # cache.set('my_Data', hasil['data'])

def save_to_file(key, value):
    with open('caches.json', 'w') as f:
        json.dump({key: value}, f)

def load_from_file(key):
    try:
        with open('caches.json', 'r') as f:
            data = json.load(f)
            return data.get(key)
    except FileNotFoundError:
        return None