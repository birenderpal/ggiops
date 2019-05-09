import json
import httplib2
import urllib
import sys
import codecs
from flask import Flask, jsonify, request
from ggiapp.controllers.Kafka import KafkaPublisher,KafkaClient
from ggiapp import app

class GGIStream():
    def __init__(self,rpcendpoint=None):

        self.rpcendpoint=app.config.get('KAFKA_API_ENDPOINT')
        
        if rpcendpoint is not None:
            self.rpcendpoint = rpcendpoint                
        
        self.INCOMING = "http://"+self.rpcendpoint+"/incoming"
        
        self.OUTGOING = "http://"+self.rpcendpoint+"/outgoing"        
    
    def get_devices(self,**karg):
        """returns all devices from incoming source and all outgoing devices
            device=device to only get details of a single device
            source=incoming/outgoing to only get devices for single source
        """
        rpc_client=KafkaClient()

        incoming_device_list = rpc_client.get_list(url=self.INCOMING,message_type="incoming",message_key="deviceName")

        outgoing_device_list = rpc_client.get_list(url=self.OUTGOING,message_type="outgoing",message_key="deviceName")

        if 'device' not in karg:

            if 'source' in karg:
                message_type=karg['source']
                url = self.OUTGOING if message_type == "outgoing" else self.INCOMING                                                    
                devices = {'count':len(outgoing_device_list),'devices':[]} if message_type == "outgoing" else {'count':len(incoming_device_list),'devices':[]} 
                
                if message_type == "outgoing":

                    for device in outgoing_device_list:
                        device_indicators=rpc_client.get_grouped_list(url=url,message_type=message_type,message_key="indicatorName",group_by=device)
                        device_details={}                    
                        device_details[device]={'count':device_indicators[device]['count'],'indicators':device_indicators[device]['list']}
                        devices['devices'].append(device_details)

                    return devices

                else:

                    for device in incoming_device_list:
                        device_indicators=rpc_client.get_grouped_list(url=url,message_type=message_type,message_key="indicatorName",group_by=device)
                        device_details={}                    
                        indicators=[] 
                        
                        if device in outgoing_device_list:                                                                                           
                            device_details[device]={'outgoing':True,'count':device_indicators[device]['count']} 
                            other_indicators=rpc_client.get_grouped_list(url=self.OUTGOING,message_type="outgoing",message_key="indicatorName",group_by=device)
                            
                            for indicator in device_indicators[device]['list']: 
                                
                                if not other_indicators:
                                    indicators.append({'indicatorName':indicator,'outgoing':False})

                                else:                                  
                                    indicators.append({'indicatorName':indicator,'outgoing':True}) \
                                        if indicator in other_indicators[device]['list'] \
                                            else indicators.append({'indicatorName':indicator,'outgoing':False})
                            device_details[device]['indicators']=indicators                            

                        else:
                            device_details[device]={'outgoing':False,'count':device_indicators[device]['count']}
                            
                            for indicator in device_indicators[device]['list']: 
                                indicators.append({'indicatorName':indicator,'outgoing':False})
                            device_details[device]['indicators']=indicators                            
                        
                        devices['devices'].append(device_details)
                    
                    return devices
            else:

                devices={'devices':
                                    {'incoming':
                                                {'count':len(incoming_device_list),
                                                'devices':[]
                                                },
                                    'outgoing':
                                                {'count':len(outgoing_device_list),
                                                'devices':[]
                                                }
                                    }
                        }                    
                for in_device in incoming_device_list:
                    device_indicators=rpc_client.get_grouped_list(url=self.INCOMING,message_type="incoming",message_key="indicatorName",group_by=in_device)
                    in_device_detail={}
                    indicators=[]

                    if in_device in outgoing_device_list:
                        in_device_detail[in_device]={'outgoing':True,'count':device_indicators[in_device]['count']}
                        outgoing_indicators=rpc_client.get_grouped_list(url=self.OUTGOING,message_type="outgoing",message_key="indicatorName",group_by=in_device)

                        for indicator in device_indicators[in_device]['list']:                                
                            indicators.append({'indicatorName':indicator,'outgoing':True}) \
                                if indicator in outgoing_indicators[in_device]['list'] \
                                    else \
                                        indicators.append({'indicatorName':indicator,'outgoing':False})                    
                            in_device_detail[in_device]['indicators']=indicators
                    
                    else:
                        in_device_detail[in_device]={'outgoing':False,'count':device_indicators[in_device]['count']}                                            
                    
                    devices['devices']['incoming']['devices'].append(in_device_detail)
                
                for out_device in outgoing_device_list:
                    device_indicators=rpc_client.get_grouped_list(url=self.OUTGOING,message_type="outgoing",message_key="indicatorName",group_by=out_device)
                    devices['devices']['outgoing']['devices'].append(\
                        {out_device:{'indicators':device_indicators[out_device]['list'],\
                        'count':device_indicators[out_device]['count']}})

                return devices
        else:
            all_devices=set()
            all_devices.update(incoming_device_list)
            all_devices.update(outgoing_device_list)
            if karg['device'] not in all_devices:
                return {}

            if 'source' in karg:
                message_type=karg['source']
                url = self.OUTGOING if message_type == "outgoing" else self.INCOMING                                                    
                device=karg['device']
                device_indicators=rpc_client.get_grouped_list(url=url,message_type=message_type,message_key="indicatorName",group_by=device)
                device_detail={}

                if message_type == "outgoing":
                    device_details[device]={'count':device_indicators[device]['count'],'indicators':device_indicators[device]['list']}

                else:
                    outgoing_indicators=rpc_client.get_grouped_list(url=self.OUTGOING,message_type="outgoing",message_key="indicatorName",group_by=device)
                    indicators=[]
                    if device in outgoing_device_list:
                        device_detail[device]={'outgoing':True,'count':device_indicators[device]['count']}

                        for indicator in device_indicators[device]['list']:    

                            if indicator in outgoing_indicators[device]['list']:
                                indicators.append({'indicatorName':indicator,'outgoing':True})

                            else:
                                indicators.append({'indicatorName':indicator,'outgoing':False})                
                        device_detail[device]['indicators']=indicators            
                    else:
                        device_detail[device]={'outgoing':False,'count':device_indicators[device]['count']}                          
                        
                        for indicator in device_indicators[device]['list']:    
                            indicators.append({'indicatorName':indicator,'outgoing':False})  
                        device_detail[device]['indicators']=indicators   

                return device_detail                      
            else:
                device=karg['device']
                device_detail={}
                indicators=[]
                device_indicators=rpc_client.get_grouped_list(url=self.INCOMING,message_type="incoming",group_by=device,message_key="indicatorName")  
                outgoing_indicators=rpc_client.get_grouped_list(url=self.OUTGOING,message_type="outgoing",group_by=device,message_key="indicatorName")  
                
                if device in outgoing_device_list:
                    device_detail[device]={'outgoing':True,'count':device_indicators[device]['count']}

                    for indicator in device_indicators[device]['list']:                                

                        if indicator in outgoing_indicators[device]['list']:
                            indicators.append({'indicatorName':indicator,'outgoing':True})

                        else:
                            indicators.append({'indicatorName':indicator,'outgoing':False})                
                
                else:
                    device_detail[device]={'outgoing':False,'count':device_indicators[device]['count']}                          
                
                    for indicator in device_indicators[device]['list']:                                
                        indicators.append({'indicatorName':indicator,'outgoing':True})
                
                device_detail[device]['indicators']=indicators            
                
                return device_detail                      
        

    def get_indicators(self,**karg):
        """returns all indicators from SevOne and all outgoing indicators to Splunk
            indicator=indicator to only get details of a single device
        """
        rpc_client=KafkaClient()
        if 'indicator' not in karg:    
            if 'source' in karg:    
                message_type=karg['source']
                url=self.OUTGOING if message_type == "outgoing" else self.INCOMING                                    
                source_indicators=rpc_client.get_list(url=url,message_type=message_type,message_key="indicatorName")
                indicators={'count':len(source_indicators),'indicators':[]}
                other_indicators = rpc_client.get_list(url=self.OUTGOING,message_type="outgoing",message_key="indicatorName") if message_type == "incoming" else None                                                                                               
                for s_indicator in source_indicators:
                    indicator_devices=rpc_client.get_grouped_list(url=url,message_type=message_type,message_key="deviceName",group_by=s_indicator)
                    indicator_detail={}
                    devices=[] 
                    if other_indicators is None:                                                                                           
                        indicator_detail[s_indicator]={'count':indicator_devices[s_indicator]['count'],'devices':indicator_devices[s_indicator]['list']}
                    else:
                        indicator_detail[s_indicator]={'outgoing':True,'count':indicator_devices[s_indicator]['count']} if s_indicator in other_indicators else {'outgoing':False,'count':indicator_devices[s_indicator]['count']}
                        other_devices=rpc_client.get_list(url=self.OUTGOING,message_type="outgoing",message_key="deviceName")
                        for device in indicator_devices[s_indicator]['list']:                               
                            devices.append({'deviceName':device,'outgoing':True}) if device in other_devices else devices.append({'deviceName':device,'outgoing':False})
                        indicator_detail[s_indicator]['devices']=devices
                                                
                    indicators['indicators'].append(indicator_detail)
                return indicators
            else:
                incoming_indicators=rpc_client.get_list(url=self.INCOMING,message_type="incoming",message_key="indicatorName")
                outgoing_indicators=rpc_client.get_list(url=self.OUTGOING,message_type="outgoing",message_key="indicatorName")
                indicators =    {'indicators':
                                    {'incoming':
                                            {'count':len(incoming_indicators),
                                             'indicators':[]
                                            },
                                     'outgoing':
                                            {'count':len(outgoing_indicators),
                                             'indicators':[]
                                            }
                                    }
                                }                    
                for in_indicator in incoming_indicators:
                    indicator_devices=rpc_client.get_grouped_list(url=self.INCOMING,message_type="incoming",message_key="deviceName",group_by=in_indicator)
                    outgoing_indicators=rpc_client.get_list(url=self.OUTGOING,message_type="outgoing",message_key="indicatorName")
                    outgoing_indicator_devices=rpc_client.get_grouped_list(url=self.OUTGOING,message_type="outgoing",message_key="deviceName",group_by=in_indicator)
                    in_indicator_detail={}
                    devices=[]
                    if in_indicator in outgoing_indicators:
                        in_indicator_detail[in_indicator]={'outgoing':True,'count':indicator_devices[in_indicator]['count']}
                    else:
                        in_indicator_detail[in_indicator]={'outgoing':False,'count':indicator_devices[in_indicator]['count']}                                            
                    for device in indicator_devices[in_indicator]['list']:
                        if not outgoing_indicator_devices:
                            devices.append({'deviceName':device,'outgoing':False})
                        else:                               
                            devices.append({'deviceName':device,'outgoing':True}) if device in outgoing_indicator_devices else devices.append({'deviceName':device,'outgoing':False})                    
                        in_indicator_detail[in_indicator]['devices']=devices
                    indicators['indicators']['incoming']['indicators'].append(in_indicator_detail)

                for out_indicator in outgoing_indicators:
                    indicator_devices=rpc_client.get_grouped_list(url=self.OUTGOING,message_type="outgoing",message_key="indicatorName",group_by=out_indicator)
                    indicators['indicators']['outgoing']['indicators'].append({out_indicator:{'devices':indicator_devices[out_indicator]['list'],'count':indicator_devices[out_indicator]['count']}})
                return indicators        
        else:
            indicator=karg['indicator']
            
            if 'source' in karg:                
                url = self.INCOMING if karg['source']=="incoming" else self.OUTGOING
                indicator_detail={}
                devices=[]
                indicator_devices=rpc_client.get_grouped_list(url=url,message_type=karg['source'],group_by=indicator,message_key="deviceName")  
                outgoing_devices=rpc_client.get_grouped_list(url=self.OUTGOING,message_type="outgoing",message_key="deviceName",group_by=indicator) if karg['source']=="incoming" else None
                if outgoing_devices is None:
                    indicator_detail[indicator]={'count':indicator_devices[indicator]['count'],'devices':indicator_devices[device]['list']} 
                else:                        
                    if indicator in rpc_client.get_list(url=self.OUTGOING,message_type="outgoing",message_key="indicatorName"):
                        indicator_detail[indicator]={'outgoing':True,'count':indicator_devices[indicator]['count']}
                    else:
                        indicator_detail[indicator]={'outgoing':False,'count':indicator_devices[indicator]['count']}                          
                    for device in indicator_devices[indicator]['list']:                                
                        if device in outgoing_devices[indicator]['list']:
                            devices.append({'deviceName':device,'outgoing':True})
                        else:
                            devices.append({'deviceName':device,'outgoing':False})                
                    indicator_detail[indicator]['devices']=devices            
                return indicator_detail                      
            else:                    
                indicator_detail={}
                devices=[]
                indicator_devices=rpc_client.get_grouped_list(url=self.INCOMING,message_type="incoming",group_by=indicator,message_key="deviceName")  
                outgoing_indicators=rpc_client.get_list(url=self.OUTGOING,message_type="outgoing",message_key="indicatorName")
                indicator_outgoing_devices=rpc_client.get_grouped_list(url=self.OUTGOING,message_type="outgoing",group_by=indicator,message_key="deviceName")
                if indicator in outgoing_indicators:
                    indicator_detail[indicator]={'outgoing':True,'count':indicator_devices[indicator]['count']}
                else:
                    indicator_detail[indicator]={'outgoing':False,'count':indicator_devices[indicator]['count']}                          
                for device in indicator_devices[indicator]['list']: 
                    if not indicator_outgoing_devices:
                        devices.append({'deviceName':device,'outgoing':True})                  
                    else:
                        if device in indicator_outgoing_devices[indicator]['list']:
                            devices.append({'deviceName':indicator,'outgoing':True})
                        else:
                            devices.append({'deviceName':indicator,'outgoing':False})                
                indicator_detail[indicator]['devices']=devices            
                return indicator_detail                      

    def enable_indicator(self,indicator=None,device=None):
        kafka_publish=KafkaPublisher()
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
        kafka_publish=KafkaPublisher()
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
        kafka_publish=KafkaPublisher()
        topic="test-topic"        
        indicators=self.get_splunk_indicators()                  
        for indicator in indicators:
            message= {"deviceName":device,"indicatorName":indicator,"toSplunk":'false'}
            key=device+indicator
            kafka_publish.publish_message(topic,key=str(key),message=message)







