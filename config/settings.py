# Archivo: config/settings.py
import os
from dotenv import load_dotenv

# Carga las contraseñas del archivo .env
load_dotenv()

class Settings:
    # --- DATOS PROPIOS ---
    BASE_URL = "https://core.kiconex.com/api"
    
    USER = os.getenv("CORE_USERNAME")
    PASSWORD = os.getenv("CORE_PASSWORD")
    
    # EL ID DE TU ORGANIZACIÓN 
    DEFAULT_TENANT_UUID = "90be8c8a-f462-4a3e-afcf-d8f34094eaa8" 

    # --- ENDPOINTS (TU PARTE: Verifica que coinciden con la documentación) ---
    URL_LOGIN = f"{BASE_URL}/users/sign-in"
    URL_DEVICES = f"{BASE_URL}/devices"
    URL_M2M = f"{BASE_URL}/m2m"