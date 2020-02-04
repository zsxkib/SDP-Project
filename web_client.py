from io import BytesIO
import numpy as np
import requests

class WebClient():
    classify_route = '/classify'
    update_route = '/update/{label}'

    def __init__(self, server_url):
        self.server_url = server_url

    def classify(self, **images):
        bytesio = BytesIO()
        np.savez_compressed(bytesio, **images)
        res = requests.post(self.server_url + self.classify_route, data=bytesio.getvalue())
        return res.content.decode('utf8')

    def update(self, label):
        res = requests.get(self.server_url + self.update_route.format(label=label))
        return res.content.decode('utf8')