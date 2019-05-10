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
    def get_kafka_messages(cls,**karg):
        """get messages from kafka rpc endpoint url=url"""          
        req = httplib2.Http()
        response,messages = (req.request(karg['url'],'GET')) 
        '''
        if karg['url']=="http://localhost:8000/outgoing":
            messages={"outgoing":[
                {'deviceName':"AKBR1",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"AKBR1",'indicatorName':'indicator2',"toSplunk":True},
                {'deviceName':"AKBR1",'indicatorName':'indicator3',"toSplunk":True},
                {'deviceName':"AKBR1",'indicatorName':'indicator4',"toSplunk":True},
                {'deviceName':"AKBR2",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"AKBR3",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"AKBR4",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"AKBR5",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"TKBR1",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"SEBR1",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"HEBR1",'indicatorName':'indicator1',"toSplunk":True}
            ]}
        else:
            messages={"incoming":[
                {'deviceName':"BKBR1",'indicatorName':'indicator1'},
                {'deviceName':"CKBR1",'indicatorName':'indicator2'},
                {'deviceName':"AKBR1",'indicatorName':'indicator3',"toSplunk":True},
                {'deviceName':"DKBR1",'indicatorName':'indicator4',"toSplunk":True},
                {'deviceName':"AKBR2",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"AKBR3",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"AKBR4",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"AKBR5",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"TKBR1",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"SEBR1",'indicatorName':'indicator1',"toSplunk":True},
                {'deviceName':"HEBR1",'indicatorName':'indicator1',"toSplunk":True}
            ]}
        return (messages)
        '''
        
        return (json.loads(messages))
    
    def get_list(self,**karg):
        """returns a list with values from kafka messages, 
            url defines kafka rpc endpoint
            message_type defines message type, 
            message_key defines dict key of kafka messages"""        
        ret_list=set()
        for data in self.get_kafka_messages(url=karg['url'])[karg['message_type']]:
            ret_list.add(data[karg['message_key']])
        return list(ret_list)
    
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
