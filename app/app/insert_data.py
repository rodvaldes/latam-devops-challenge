from google.cloud import bigquery
from datetime import datetime

# Inicializar el cliente (usa GOOGLE_APPLICATION_CREDENTIALS o auth implícita)
client = bigquery.Client()

# Definir tabla destino
table_id = "cyberstage.challenge.raw_events"

# Crear lista de diccionarios con los datos
rows_to_insert = [
    {"flight_id": "flight1", "status": "ontime", "timestamp": "2024-01-01T00:00:00"},
    {"flight_id": "flight2", "status": "delayed", "timestamp": "2024-01-02T00:00:00"},
    {"flight_id": "flight3", "status": "cancelled", "timestamp": "2024-01-03T00:00:00"},
    {"flight_id": "flight4", "status": "ontime", "timestamp": "2024-01-04T00:00:00"},
    {"flight_id": "flight5", "status": "delayed", "timestamp": "2024-01-05T00:00:00"},
    {"flight_id": "flight6", "status": "delayed", "timestamp": "2024-01-06T00:00:00"},
    {"flight_id": "flight7", "status": "ontime", "timestamp": "2024-01-07T00:00:00"},
    {"flight_id": "flight8", "status": "cancelled", "timestamp": "2024-01-08T00:00:00"},
    {"flight_id": "flight9", "status": "ontime", "timestamp": "2024-01-09T00:00:00"},
    {"flight_id": "flight10", "status": "delayed", "timestamp": "2024-01-10T00:00:00"},
]

# Insertar filas
errors = client.insert_rows_json(table_id, rows_to_insert)

# Verificar errores
if errors == []:
    print("✅ Registros insertados correctamente.")
else:
    print("❌ Ocurrieron errores:")
    print(errors)
