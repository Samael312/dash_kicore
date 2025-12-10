# Archivo: backend/api_client.py
import requests
from config.settings import Settings
import pandas as pd

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

    def get_m2m(self):
        if not self.token:
            return []
        url = f"{Settings.URL_M2M}?tenant_uuid={Settings.DEFAULT_TENANT_UUID}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()

            # Mostrar columnas y primeros 5 valores
            self._export_columns_to_excel(data, filename= "m2m.xlsx")

            return data
        return []
    
    def get_devicesB(self):
        if not self.token:
            return []
        resp = requests.get(Settings.URL_DEVICES, headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()

            self._export_columns_to_excel(data, filename= "boards.xlsx")

            return data
        return []
    
    def get_devicesKiwi(self):
        if not self.token:
            return []
        resp = requests.get(Settings.URL_DEVICES2, headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()

            self._export_columns_to_excel(data, filename= "kiwi.xlsx")

            return data
        return []
    
    def get_deviceInfo(self):
        if not self.token:
            return []
        resp = requests.get(Settings.URL_INFO, headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()

            self._export_columns_to_excel(data, filename= "info.xlsx")

            return data
        return []

    def _export_columns_to_excel(self, data, filename="output.xlsx"):
        if not isinstance(data, list) or len(data) == 0 or not isinstance(data[0], dict):
            print("Formato de datos no compatible para exportar a Excel")
            return

        # Tomamos solo los primeros 5 registros
        sample_data = data

        # Convertimos a DataFrame
        df = pd.DataFrame(sample_data)

        # Guardamos en Excel
        df.to_excel(filename, index=False)
        print(f"Datos exportados a {filename}")