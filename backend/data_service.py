import pandas as pd

def process_devices(json_data):
    if not json_data: return pd.DataFrame()
    df = pd.DataFrame(json_data)
    
    # 1. ORGANIZACIÓN
    # Tu API no devuelve el nombre de la empresa, solo el ID (tenant_uuid).
    # Usaremos el ID por ahora.
    if 'tenant_uuid' in df.columns:
        df['organization'] = df['tenant_uuid'] # Renombramos conceptualmente
    else:
        df['organization'] = 'Desconocida'

    # 2. MODELO
    # No hay columna 'model'. Usaremos '_type' o 'description' como parche.
    if '_type' in df.columns:
        df['model'] = df['_type']
    else:
        df['model'] = 'Genérico'
        
    # 3. ESTADO (Limpieza)
    # A veces viene como True/False, lo convertimos a texto para que el gráfico se entienda
    if 'status' in df.columns:
        df['status'] = df['status'].apply(lambda x: 'Conectado' if x else 'Desconectado')
        
    return df

def process_m2m(json_data):
    if not json_data: return pd.DataFrame()
    df = pd.DataFrame(json_data)
    
    # 1. ESTADO (lifeCycleStatus)
    if 'lifeCycleStatus' in df.columns:
        df['status_clean'] = df['lifeCycleStatus'].fillna('DESCONOCIDO')
    else:
        df['status_clean'] = 'DESCONOCIDO'

    # 2. TARIFA (servicePack)
    if 'servicePack' in df.columns:
        df['rate_plan'] = df['servicePack'].fillna('Sin Plan')
    else:
        df['rate_plan'] = 'N/A'

    # 3. TECNOLOGÍA / RED (ratType)
    # Usaremos esto en lugar de "País" por ahora, ya que el país no viene explícito
    if 'ratType' in df.columns:
        df['network_type'] = df['ratType'].fillna('N/A')
    else:
        df['network_type'] = 'N/A'

    # 4. ORGANIZACIÓN (commercialGroupId)
    if 'commercialGroupId' in df.columns:
        df['organization'] = df['commercialGroupId'].astype(str)
    else:
        df['organization'] = 'General'

    # 5. CONSUMOS (Limpieza básica)
    # A veces vienen como strings "0 bytes". Intentamos limpiar o lo dejamos tal cual.
    # Por ahora solo aseguramos que la columna exista.
    if 'consumptionDaily' not in df.columns:
        df['consumptionDaily'] = 0

    return df