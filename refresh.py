import requests
import json
from datetime import date
from secrets import refresh_token, client_B64 

class Refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.client_B64 = client_B64
    
    def refresh(self):
        url = "https://accounts.spotify.com/api/token"
        request_body = {
            "grant_type": "refresh_token",
            "refresh_token": f"{self.refresh_token}"
            }
        headers = {
            "Authorization": f"Basic {self.client_B64}"
            }

        response = requests.post(url, data=request_body, headers=headers)
        token = response.json()["access_token"] 
        return token