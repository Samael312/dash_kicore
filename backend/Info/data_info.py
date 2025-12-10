import pandas as pd
import json

def safe_json(x):
    """Convierte strings JSON a dict. Si falla → None"""
    if isinstance(x, dict):
        return x
    if isinstance(x, str):
        # Maneja strings vacíos y la corrección de comillas simples (' a ")
        if not x.strip():
            return None
        try: 
            # Reemplazo de comillas simples por dobles, común en datos exportados
            return json.loads(x.replace("'", '"')) 
        except:
            return None
    return None


def extract_version(json_obj):
    """Extrae la versión 'quiiotd_version' del diccionario de información."""
    if not isinstance(json_obj, dict):
        return None
    # Usamos .get() directamente para manejo seguro de claves
    return json_obj.get("quiiotd_version", None)
    
def extract_compilation(json_obj):
    """Extrae la fecha de compilación 'compilation_date' del diccionario de información."""
    if not isinstance(json_obj, dict):
        return None
    return json_obj.get("compilation_date", None)

def process_devicesInfo(json_data, info_column_name='info'):
    """
    Procesa los datos crudos, extrae y normaliza las columnas de versión 
    y fecha de compilación del JSON anidado.
    """
    if not json_data:
        return pd.DataFrame()

    df = pd.DataFrame(json_data)
    
    # Aseguramos que la columna 'info' exista antes de procesar
    if "info" not in df.columns:
     
        df["info"] = None
     
        df['quiiotd_version'] = None
        df['compilation_date'] = None
        return df

    # 1. Aplicamos safe_json a la columna que contiene el JSON (asumimos 'info')
    df['info_json'] = df["info"].apply(safe_json)
    
    # 2. Aplicamos las funciones de extracción a la nueva columna 'info_json'
    df['quiiotd_version'] = df['info_json'].apply(extract_version)
    df['compilation_date'] = df['info_json'].apply(extract_compilation)
    
    # Opcional: Eliminar la columna intermedia si ya no se necesita
    df = df.drop(columns=['info_json'], errors='ignore')

    return df