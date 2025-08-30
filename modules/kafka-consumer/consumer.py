import json
from kafka import KafkaConsumer
from service import save_kafka_event

consumer = KafkaConsumer(
    'locations',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    save_kafka_event(message.value)
