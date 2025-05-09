from google.cloud import pubsub_v1
from google.cloud import bigquery
import json
import os

# Configura tus variables
project_id = "cyberstage"         # ⚠️ Cambia esto
subscription_id = "flight-events-sub"
dataset_id = "core"
table_id = "raw_events"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

bq_client = bigquery.Client(project=project_id)
table_ref = bq_client.dataset(dataset_id).table(table_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print("📨 Mensaje recibido")

    try:
        data = json.loads(message.data.decode("utf-8"))

        row = {
            "flight_id": data.get("flight_id"),
            "status": data.get("status"),
            "timestamp": data.get("timestamp")
        }

        errors = bq_client.insert_rows_json(table_ref, [row])
        if errors:
            print("❌ Error al insertar en BigQuery:", errors)
        else:
            print("✅ Mensaje insertado en BigQuery:", row)

        message.ack()

    except Exception as e:
        print("❌ Error procesando mensaje:", e)

print(f"🔔 Escuchando suscripción: {subscription_path}")
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    print("🛑 Suscriptor detenido por el usuario.")
