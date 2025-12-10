import pandas as pd
import json

import pandas as pd

def process_devices(data):
    """
    Procesa datos crudos (lista de dicts o DataFrame) y normaliza columnas.
    """
    # 1. Convertir a DataFrame si es una lista (JSON)
    if isinstance(data, list):
        if not data: # Si la lista está vacía
            return pd.DataFrame()
        df = pd.DataFrame(data)
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        # Si llega algo nulo o desconocido
        return pd.DataFrame()

    # 2. Verificar si el DF está vacío después de la conversión
    if df.empty:
        return df

    # --- Lógica de Limpieza y Normalización ---
    
    # ORGANIZACIÓN: Buscamos la columna más adecuada según el archivo (Boards o Kiwi)
    if "final_client" in df.columns:
        df["organization"] = df["final_client"].fillna("Sin Asignar")
    elif "name" in df.columns:
        df["organization"] = df["name"].fillna("Sin Asignar")
    elif "order_id" in df.columns:
        df["organization"] = df["order_id"].fillna("Sin Asignar") # Kiwi suele usar order_id
    else:
        df["organization"] = "Desconocida"

    # MODELO: Boards tiene 'model', Kiwi no (usamos Genérico o derivado)
    if "model" in df.columns:
        df["model"] = df["model"].fillna("Genérico")
    elif "ssid" in df.columns:
        df["model"] = df["software"].fillna("Genérico")

    # ESTADO (Status): Normalizamos la columna 'state' o 'status'
    col_state = "state" if "state" in df.columns else "status"
    
    def get_status_label(val):
        s = str(val).lower()
        if s in ["terminado", "online", "connected", "true"]:
            return "Conectado"
        return "Desconectado"

    def get_enabled_label(val):
        s = str(val).lower()
        if s in ["terminado", "asignado", "fabricado", "true", "enabled"]:
            return "Habilitado"
        return "Deshabilitado"

    # Aplicamos la limpieza solo si existe la columna origen
    if col_state in df.columns:
        df["status_clean"] = df[col_state].apply(get_status_label)
        df["enabled_clean"] = df[col_state].apply(get_enabled_label)
    else:
        df["status_clean"] = "Desconectado"
        df["enabled_clean"] = "Deshabilitado"

    return df