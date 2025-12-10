import pandas as pd

def prepare_boards(data):
    """
    Prepara un DataFrame de Boards desde lista de dicts o DataFrame.
    Agrega: model, organization, status_clean, enabled_clean
    """
    # Convertir lista a DataFrame si es necesario
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        return pd.DataFrame()

    if df.empty:
        return df

    # Model: usamos 'name' o 'ki_id' si existe
    if "name" in df.columns:
        df["model"] = df["name"].fillna("Genérico")
    elif "ki_id" in df.columns:
        df["model"] = df["ki_id"].fillna("Genérico")
    else:
        df["model"] = "Genérico"

    # Organization: usamos 'final_client' si existe
    df["organization"] = df["final_client"].fillna("Sin Asignar") if "final_client" in df.columns else "Sin Asignar"

    # Status y Enabled
    col_state = "state" if "state" in df.columns else "status"

    def get_status_label(val):
        s = str(val).lower()
        return "Conectado" if s in ["terminado", "online", "connected", "true"] else "Desconectado"

    def get_enabled_label(val):
        s = str(val).lower()
        return "Habilitado" if s in ["terminado", "asignado", "fabricado", "true", "enabled"] else "Deshabilitado"

    df["status_clean"] = df[col_state].apply(get_status_label) if col_state in df.columns else "Desconectado"
    df["enabled_clean"] = df[col_state].apply(get_enabled_label) if col_state in df.columns else "Deshabilitado"

    return df


def prepare_kiwi(data):
    """
    Prepara un DataFrame de Kiwi desde lista de dicts o DataFrame.
    Agrega: model, organization, status_clean, enabled_clean
    """
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        return pd.DataFrame()

    if df.empty:
        return df

    # Model: usamos 'ssid'
    df["model"] = df["ssid"].fillna("Genérico") if "ssid" in df.columns else "Genérico"

    # Organization: asignamos genérico
    df["organization"] = "Sin Asignar"

    # Status y Enabled
    col_state = "state" if "state" in df.columns else "status"

    def get_status_label(val):
        s = str(val).lower()
        return "Conectado" if s in ["terminado", "online", "connected", "true"] else "Desconectado"

    def get_enabled_label(val):
        s = str(val).lower()
        return "Habilitado" if s in ["terminado", "asignado", "fabricado", "true", "enabled"] else "Deshabilitado"

    df["status_clean"] = df[col_state].apply(get_status_label) if col_state in df.columns else "Desconectado"
    df["enabled_clean"] = df[col_state].apply(get_enabled_label) if col_state in df.columns else "Deshabilitado"

    return df
