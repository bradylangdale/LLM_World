import requests

class Oobabooga:

    def __init__(self, ip='localhost', port='5000') -> None:
        self.ip = ip
        self.port = port

        self.url = f'http://{self.ip}:{self.port}/v1/'

    def get_models(self):
        response = requests.get(self.url + 'internal/model/list')
        return response.json()['model_names']
    
    def load_model(self, args_json={}):
        response = requests.post(self.url + 'internal/model/load/', json=args_json)
        return response.json()
    
    def unload_model(self, args_json={}):
        response = requests.post(self.url + 'internal/model/unload/', json=args_json)
        return response.json()
    
    def get_model_info(self):
        response = requests.get(self.url + 'internal/model/info')
        return response.json()
    
    def stop_generation(self):
        response = requests.post(self.url + 'internal/stop-generation')
        return response.json()
    
    def chat_completion(self, args_json={}, stream=False):
        if not stream:
            response = requests.post(self.url + 'chat/completions', json=args_json)
            return response.json()
        else:
            return requests.post(self.url + 'chat/completions',
                                 headers={ "Content-Type": "application/json" },
                                 json=args_json,
                                 verify=False,
                                 stream=True)
    
    def completion(self, args_json={}, stream=False):
        if not stream:
            response = requests.post(self.url + 'completions', json=args_json)
            return response.json()
        else:
            return requests.post(self.url + 'completions',
                                 headers={ "Content-Type": "application/json" },
                                 json=args_json,
                                 verify=False,
                                 stream=True)