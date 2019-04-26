import json
from time import sleep
from kafka import KafkaConsumer, KafkaProducer

class KafkaPublisher():
    def __init__(self,bootstrap_servers):
        print(bootstrap_servers)        
        try:
            self._producer = KafkaProducer(bootstrap_servers=bootstrap_servers,key_serializer=str.encode,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            #self._producer = KafkaProducer(bootstrap_servers=bootstrap_servers,key_serializer=str.encode)
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
        #print(self._producer)
    def publish_message(self,topic, key, message):        
        try:
            print(topic)
            print(message)
            #message=json.loads(message)
            print(key)
            #print(self._producer)
            self._producer.send(topic,key=key,value=message)            
            #self._producer.send(topic_name, key=key, value=value)
            self._producer.flush()            
            print("Message published")
        except Exception as ex:            
            print(str(ex))
    