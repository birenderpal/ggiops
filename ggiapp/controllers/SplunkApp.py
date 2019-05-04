import json
import httplib2
import urllib
import sys
import codecs
from flask import Flask, jsonify, request
from ggiapp.controllers.KafkaPublisher import KafkaPublisher

class SplunkApp():
    def __init__(self,rpcendpoint):                
        self.INVENTORY_URL = "http://"+rpcendpoint+"/inventory"
        self.MESSAGES_URL = "http://"+rpcendpoint+"/messages"
        self.req = httplib2.Http() 

    def get_kafka_messages(self):
        response,messages = (self.req.request(self.MESSAGES_URL,'GET')) 
        return json.loads(messages)['messages']      
    def get_sevone_inventory(self):        
        response,inventory = (self.req.request(self.INVENTORY_URL,'GET'))        
        return json.loads(inventory)['inventory']
    def get_sevone_devices(self):        
        devices=set()
        INVENTORY = self.get_sevone_inventory()
        for data in INVENTORY:
            devices.add(data['deviceName'])
        return list(devices)

    def get_sevone_device(self,device):        
        indicator_list=[]
        dev_list=[]
        INVENTORY = self.get_sevone_inventory()
        for inventory in INVENTORY:
            if inventory['deviceName']==device:
                dev_list.append(device)
                indicator_list.append(inventory['indicatorName'])
        if dev_list:
            device_details={device:{"indicators":indicator_list}}
        else:
            device_details={}            
        return device_details                            
    def get_sevone_indicator(self,indicator):        
        device_list=[]
        ind_list=[]
        INVENTORY = self.get_sevone_inventory()
        for inventory in INVENTORY:
            if inventory['indicatorName']==indicator:
                ind_list.append(indicator)
                device_list.append(inventory['deviceName'])
        if ind_list:
            indicator_details={indicator:{"devices":device_list}}
        else:
            indicator_details={}
        return indicator_details       

    def get_sevone_indicators(self,device=None):
        indicators=set()
        INVENTORY = self.get_sevone_inventory()
        for data in INVENTORY:
            if device is None:
                indicators.add(data['indicatorName'])
            else:
                if device == data['deviceName']:
                    indicators.add(data['indicatorName'])
        return list(indicators)

    def enable_indicator(self,indicator=None,device=None):
        #bootstrap_server=['10.235.116.68:9092','10.235.116.67:9092','10.236.132.75:9092']
        bootstrap_server=['capltda28.telecom.tcnz.net:9092']        
        kafka_publish=KafkaPublisher(bootstrap_server)
        topic="test-topic"
        if device is None and indicator is None:
            raise Exception('Invalid method call')
        if device is None:
            devices=self.get_sevone_devices()
            indicators=[indicator]                  
        else:
            devices=[str(device)]            
        if indicator is None:
            indicators=self.get_sevone_indicators(device)
            devices=[device]
        else:            
            indicators=[str(indicator)]
        for d in devices:
            for i in indicators:
                message= {"deviceName":d,"indicatorName":i,"toSplunk":'true'}
                key=d+i
                kafka_publish.publish_message(topic,key=str(key),message=message)              
        
    def disable_indicator(self,indicator=None,device=None):
        #bootstrap_server=['10.235.116.68:9092','10.235.116.67:9092','10.236.132.75:9092']
        bootstrap_server=["capltda28:9092"]
        kafka_publish=KafkaPublisher(bootstrap_server)
        topic="test-topic"
        if device is None and indicator is None:
            raise Exception('Invalid method call')
        if device is None:
            devices=self.get_sevone_devices()                  
        else:
            devices=[str(device)]            
        if indicator is None:
            indicators=self.get_splunk_indicators()
        else:
            indicators=[indicator]
        for d in devices:
            for i in indicators:
                message= {"deviceName":d,"indicatorName":i,"toSplunk":'false'}
                key=d+i
                kafka_publish.publish_message(topic,key=str(key),message=message)

    def disable_device(self,device):
        #bootstrap_server=['10.235.116.68:9092','10.235.116.67:9092','10.236.132.75:9092']
        bootstrap_server=["capltda28:9092"]
        kafka_publish=KafkaPublisher(bootstrap_server)
        topic="test-topic"        
        indicators=self.get_splunk_indicators()                  
        for indicator in indicators:
            message= {"deviceName":device,"indicatorName":indicator,"toSplunk":'false'}
            key=device+indicator
            kafka_publish.publish_message(topic,key=str(key),message=message)

    def get_splunk_devices(self):        
        devices=set()
        MESSAGES=self.get_kafka_messages()
        for data in MESSAGES:
            devices.add(data['deviceName'])
        return list(devices)
    def get_splunk_device(self,device):        
        indicator_list=[]
        dev_list=[]
        MESSAGES=self.get_kafka_messages()
        for message in MESSAGES:
            if message['deviceName']==device:
                dev_list.append(device)
                indicator_list.append(message['indicatorName'])
        if dev_list:            
            device_details={device:{"indicators":indicator_list}}
        else:
            device_details={}            
        return device_details
    def get_splunk_indicator(self,indicator):        
        device_list=[]
        indicator_list=[]
        MESSAGES=self.get_kafka_messages()
        for message in MESSAGES:
            if message['indicatorName']==indicator:
                indicator_list.append(indicator)
                device_list.append(message['deviceName'])
        if indicator_list:
            indicator_details={indicator:{"devices":device_list}}
        else:
            indicator_details={}
        return indicator_details
    def get_splunk_indicators(self):
        indicators=set()
        MESSAGES=self.get_kafka_messages()
        for message in MESSAGES:
            indicators.add(message['indicatorName'])
        return list(indicators)






