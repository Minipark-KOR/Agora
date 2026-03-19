import requests

class NotifierClient:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def send_alert(self, text):
        requests.post(f"{self.api_url}/v1/notify", 
                      headers={"Authorization": f"Bearer {self.api_key}"},
                      json={"text": text})
