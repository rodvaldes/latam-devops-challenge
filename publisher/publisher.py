from google.cloud import pubsub_v1
import json

project_id = "cyberstage"
topic_id = "flight-events"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

message_dict = {
    "flight_id": "UX133",
    "status": "ON_TIME",
    "timestamp": "2025-05-04T17:00:00Z"
}

message_bytes = json.dumps(message_dict).encode("utf-8")

future = publisher.publish(topic_path, data=message_bytes)
print(f"Mensaje publicado: {future.result()}")