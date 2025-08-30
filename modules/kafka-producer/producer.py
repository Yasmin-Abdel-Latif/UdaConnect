from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def publish_to_kafka(topic, message):
    retry = 3
    while retry > 0:
        try:
            producer.send(topic, message)
            producer.flush()
            break
        except Exception as e:
            retry -= 1
            time.sleep(1)
            if retry == 0:
                raise e
