import json
import httplib2
import urllib
import sys
import codecs
from flask import Flask, jsonify, request


class SevOne():
    def __init__(self,rpcendpoint):                
        self.INVENTORY_URL = "http://"+rpcendpoint+"/inventory"
        req = httplib2.Http();        
        response,content = (req.request(self.INVENTORY_URL,'GET'))        
        self.INVENTORY = json.loads(content)['inventory']
    def get_sevone_devices(self):        
        devices=set()
        for data in self.INVENTORY:
            devices.add(data['deviceName'])
        return list(devices)

    def get_sevone_device_metrics(self,device):        
        indicator_list=[]
        for inventory in self.INVENTORY:
            if inventory['deviceName']==device:
                indicator_list.append(inventory['indicatorName'])
        device_details={device:indicator_list}                   
        return device_details
    def get_sevone_indicators(self):
        indicators=set()
        for data in self.INVENTORY:
            indicators.add(data['indicatorName'])
        return list(indicators)






