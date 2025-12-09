# Archivo: backend/api_client.py
import requests
from config.settings import Settings

class CoreClient:
    def __init__(self, token=None):
        self.token = token
        # 'Authorization': 'Basic tuTokenDeSesion'
        self.headers = {
            'Authorization': f"Basic {self.token}"
        } if token else {}

    def login(self):
        """Hace login y devuelve el apiToken"""
        payload = {"username": Settings.USER, "password": Settings.PASSWORD}
        try:
            response = requests.post(Settings.URL_LOGIN, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get("login") is True:
                    return data.get("apiToken")
            return None
        except Exception as e:
            print(f"Error login: {e}")
            return None

    def get_devices(self):
        if not self.token: return []
        resp = requests.get(Settings.URL_DEVICES, headers=self.headers)
        return resp.json() if resp.status_code == 200 else []

    def get_m2m(self):
        if not self.token: return []
        # Usa el UUID que configuramos en settings.py
        url = f"{Settings.URL_M2M}?tenant_uuid={Settings.DEFAULT_TENANT_UUID}"
        resp = requests.get(url, headers=self.headers)
        return resp.json() if resp.status_code == 200 else []