import json
from dotenv import load_dotenv
import os
import base64
from requests import post
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_access_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = {
        "Authorization": f'Basic {base64.b64encode((client_id + ":" + client_secret).encode()).decode()}'
    }
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    auth_response = requests.post(auth_url, data=auth_data, headers=auth_header)
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    return access_token