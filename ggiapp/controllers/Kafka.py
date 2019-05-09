import json
import httplib2
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
from ggiapp import app
class KafkaPublisher():
    def __init__(self,bootstrap_servers=None):     
        self.bootstrap_servers=app.config.get('BOOTSTRAP_SERVERS')
        if bootstrap_servers is not None:
            self.bootstrap_servers=bootstrap_servers
        try:
            self._producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,key_serializer=str.encode,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        except Exception as ex:
            print(str(ex))
        #print(self._producer)
    def publish_message(self,topic, key, message):        
        try:
            self._producer.send(topic,key=key,value=message)            
            self._producer.flush()            
        except Exception as ex:            
            print(str(ex))
class KafkaClient():
    
    def __init__(self):
        self.req = httplib2.Http()

    @classmethod
    def get_kafka_messages(self,**karg):
        self.req = httplib2.Http()
        """get messages from kafka rpc endpoint url=url"""          
        response,messages = (self.req.request(karg['url'],'GET')) 
        return json.loads(messages)
    @classmethod
    def get_list(self,**karg):
        """returns a list with values from kafka messages, 
            url defines kafka rpc endpoint
            message_type defines message type, 
            message_key defines dict key of kafka messages"""        
        ret_list=set()
        for data in self.get_kafka_messages(url=karg['url'])[karg['message_type']]:
            ret_list.add(data[karg['message_key']])
        return list(ret_list)
    @classmethod
    def get_grouped_list(self,**karg):
        """returns a dictionary with values grouped from kafka messages, 
            url defines kafka rpc endpoint
            message_type defines message type,              
            group_by defines dict item to use for grouping of kafka messages
            message_key defines dict key of kafka messages value of which will be in the list
            """        
        ret_dict={}
        ret_list=[]
        for data in self.get_kafka_messages(url=karg['url'])[karg['message_type']]:
            for key,value in data.items():
                if value == karg['group_by']:                    
                    ret_list.append(data[karg['message_key']])
        ret_dict[karg['group_by']]={'count':len(ret_list),'list':ret_list}
        return ret_dict
