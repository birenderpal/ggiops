import json
import httplib2
import urllib
import sys
import codecs
from flask import Flask, jsonify, request
from KafkaFilterApp.controllers.Kafka import KafkaPublisher, KafkaClient
from KafkaFilterApp import app


class GGIStream():
    def __init__(self, rpcendpoint=None):

        self.rpcendpoint = app.config.get('KAFKA_API_ENDPOINT')

        if rpcendpoint is not None:
            self.rpcendpoint = rpcendpoint

        self.INCOMING = "http://"+self.rpcendpoint+"/incoming"

        self.OUTGOING = "http://"+self.rpcendpoint+"/outgoing"

    def get_devices(self, **karg):
        """returns all devices from incoming source and all outgoing devices
            device=device to only get details of a single device
            source=incoming/outgoing to only get devices for single source
        """
        rpc_client = KafkaClient()

        incoming_device_list = rpc_client.get_list(
            url=self.INCOMING, message_type="incoming", message_key="deviceName")

        outgoing_device_list = rpc_client.get_list(
            url=self.OUTGOING, message_type="outgoing", message_key="deviceName")

        if 'device' not in karg:
            device = {}

            if 'source' in karg:
                message_type = karg['source']
                url = self.OUTGOING if message_type == "outgoing" else self.INCOMING
                devices = {'count': len(outgoing_device_list), 'devices': []} if message_type == "outgoing" else {
                    'count': len(incoming_device_list), 'devices': []}

                if message_type == "outgoing":

                    for device in outgoing_device_list:
                        device_indicators = rpc_client.get_grouped_list(
                            url=url, message_type=message_type, message_key="indicatorName", group_by=device)
                        device_details = {}
                        indicators =[]

                        for indicator in device_indicators[device]['list']:
                            indicators.append({'indicatorName':indicator,'outgoing':True})
                        device_details[device] = {
                            'count': device_indicators[device]['count'], 'indicators': indicators,'outgoing':True}
                        devices['devices'].append(device_details)

                else:

                    for device in incoming_device_list:
                        device_indicators = rpc_client.get_grouped_list(
                            url=url, message_type=message_type, message_key="indicatorName", group_by=device)
                        device_details = {}
                        indicators = []

                        if device in outgoing_device_list:
                            device_details[device] = {
                                'outgoing': True, 'count': device_indicators[device]['count']}
                            device_outgoing_indicators = rpc_client.get_grouped_list(
                                url=self.OUTGOING, message_type="outgoing", message_key="indicatorName", group_by=device)

                            for indicator in device_indicators[device]['list']:

                                if not device_outgoing_indicators:
                                    indicators.append(
                                        {'indicatorName': indicator, 'outgoing': False})

                                else:
                                    indicators.append({'indicatorName': indicator, 'outgoing': True}) \
                                        if indicator in device_outgoing_indicators[device]['list'] \
                                        else indicators.append({'indicatorName': indicator, 'outgoing': False})
                            device_details[device]['indicators'] = indicators

                        else:
                            device_details[device] = {
                                'outgoing': False, 'count': device_indicators[device]['count']}

                            for indicator in device_indicators[device]['list']:
                                indicators.append(
                                    {'indicatorName': indicator, 'outgoing': False})
                            device_details[device]['indicators'] = indicators

                        devices['devices'].append(device_details)

            else:

                devices = {'devices':
                           {'incoming':
                            {'count': len(incoming_device_list),
                             'devices': []
                             },
                            'outgoing':
                            {'count': len(outgoing_device_list),
                             'devices': []
                             }
                            }
                           }
                for in_device in incoming_device_list:
                    device_indicators = rpc_client.get_grouped_list(
                        url=self.INCOMING, message_type="incoming", message_key="indicatorName", group_by=in_device)
                    in_device_detail = {}
                    indicators = []

                    if in_device in outgoing_device_list:
                        in_device_detail[in_device] = {
                            'outgoing': True, 'count': device_indicators[in_device]['count']}
                        outgoing_indicators = rpc_client.get_grouped_list(
                            url=self.OUTGOING, message_type="outgoing", message_key="indicatorName", group_by=in_device)

                        for indicator in device_indicators[in_device]['list']:
                            indicators.append({'indicatorName': indicator, 'outgoing': True}) \
                                if indicator in outgoing_indicators[in_device]['list'] \
                                else \
                                indicators.append(
                                    {'indicatorName': indicator, 'outgoing': False})
                            in_device_detail[in_device]['indicators'] = indicators

                    else:
                        in_device_detail[in_device] = {
                            'outgoing': False, 'count': device_indicators[in_device]['count']}

                    devices['devices']['incoming']['devices'].append(
                        in_device_detail)

                for out_device in outgoing_device_list:
                    device_indicators = rpc_client.get_grouped_list(
                        url=self.OUTGOING, message_type="outgoing", message_key="indicatorName", group_by=out_device)
                    devices['devices']['outgoing']['devices'].append(
                        {out_device: {'indicators': device_indicators[out_device]['list'],
                                      'count': device_indicators[out_device]['count']}})

            return devices

        else:
            all_devices = set()
            all_devices.update(incoming_device_list)
            all_devices.update(outgoing_device_list)
            device_details = {}
            if karg['device'] not in all_devices:
                return device_details

            if 'source' in karg:
                message_type = karg['source']
                url = self.OUTGOING if message_type == "outgoing" else self.INCOMING
                device = karg['device']
                device_indicators = rpc_client.get_grouped_list(
                    url=url, message_type=message_type, message_key="indicatorName", group_by=device)

                if message_type == "outgoing":
                    
                    if device not in outgoing_device_list:
                        return device_details
                    indicators =[]

                    for indicator in device_indicators[device]['list']:
                        indicators.append({'indicatorName':indicator,'outgoing':True})

                    device_details[device] = {
                        'count': device_indicators[device]['count'], 'indicators': indicators,'outgoing':True}

                else:
                    if device not in incoming_device_list:
                        return device_details
                        
                    outgoing_indicators = rpc_client.get_grouped_list(
                        url=self.OUTGOING, message_type="outgoing", message_key="indicatorName", group_by=device)
                    indicators = []
                    if device in outgoing_device_list:
                        device_details[device] = {
                            'outgoing': True, 'count': device_indicators[device]['count']}

                        for indicator in device_indicators[device]['list']:

                            if indicator in outgoing_indicators[device]['list']:
                                indicators.append(
                                    {'indicatorName': indicator, 'outgoing': True})

                            else:
                                indicators.append(
                                    {'indicatorName': indicator, 'outgoing': False})
                        device_details[device]['indicators'] = indicators
                    else:
                        device_details[device] = {
                            'outgoing': False, 'count': device_indicators[device]['count']}

                        for indicator in device_indicators[device]['list']:
                            indicators.append(
                                {'indicatorName': indicator, 'outgoing': False})
                        device_details[device]['indicators'] = indicators

            else:
                device = karg['device']
                indicators = []
                device_indicators = rpc_client.get_grouped_list(
                    url=self.INCOMING, message_type="incoming", group_by=device, message_key="indicatorName")
                outgoing_indicators = rpc_client.get_grouped_list(
                    url=self.OUTGOING, message_type="outgoing", group_by=device, message_key="indicatorName")

                if device in outgoing_device_list:
                    device_details[device] = {
                        'outgoing': True, 'count': device_indicators[device]['count']}

                    for indicator in device_indicators[device]['list']:

                        if indicator in outgoing_indicators[device]['list']:
                            indicators.append(
                                {'indicatorName': indicator, 'outgoing': True})

                        else:
                            indicators.append(
                                {'indicatorName': indicator, 'outgoing': False})

                else:
                    device_details[device] = {
                        'outgoing': False, 'count': device_indicators[device]['count']}

                    for indicator in device_indicators[device]['list']:
                        indicators.append(
                            {'indicatorName': indicator, 'outgoing': True})

                device_details[device]['indicators'] = indicators

            return device_details

    def get_indicators(self, **karg):
        """returns all indicators from SevOne and all outgoing indicators to Splunk
            indicator=indicator to only get details of a single device
        """
        rpc_client = KafkaClient()

        incoming_indicators_list = rpc_client.get_list(
            url=self.INCOMING, message_type="incoming", message_key="indicatorName")

        outgoing_indicators_list = rpc_client.get_list(
            url=self.OUTGOING, message_type="outgoing", message_key="indicatorName")

        if 'indicator' not in karg:
            indicators = {}

            if 'source' in karg:
                message_type = karg['source']
                url = self.OUTGOING if message_type == "outgoing" else self.INCOMING
                indicators = {'count': len(outgoing_indicators_list), 'indicators': []} \
                    if message_type == "outgoing" \
                    else {'count': len(incoming_indicators_list), 'indicators': []}

                if message_type == "outgoing":

                    for indicator in outgoing_indicators_list:
                        indicator_devices = rpc_client.get_grouped_list(
                            url=url, message_type=message_type, message_key="deviceName", group_by=indicator)
                        indicator_details = {}
                        devices=[]
                        for device in indicator_devices[indicator]['list']:
                            devices.append({'deviceName':device,'outgoing':True})
                        indicator_details[indicator] = {
                            'count': indicator_devices[indicator]['count'], 'devices': devices,'outgoing':True}
                        indicators['indicators'].append(indicator_details)

                else:

                    for indicator in incoming_indicators_list:
                        indicator_devices = rpc_client.get_grouped_list(
                            url=url, message_type=message_type, message_key="deviceName", group_by=indicator)

                        indicator_details = {}
                        devices = []

                        if indicator in outgoing_indicators_list:
                            indicator_outgoing_devices = rpc_client.get_grouped_list(
                                url=self.OUTGOING, message_type="outgoing", message_key="deviceName", group_by=indicator)
                            indicator_details[indicator] = {
                                'outgoing': True, 'count': indicator_devices[indicator]['count']}

                            for device in indicator_devices[indicator]['list']:

                                if device in indicator_outgoing_devices[indicator]['list']:
                                    devices.append(
                                        {'deviceName': device, 'outgoing': True})
                                else:
                                    devices.append(
                                        {'deviceName': device, 'outgoing': False})
                            indicator_details[indicator]['devices'] = devices
                        else:                            
                            indicator_details[indicator] = {
                                'outgoing': False, 'count': indicator_devices[indicator]['count']}

                            for device in indicator_devices[indicator]['list']:
                                devices.append({'deviceName': device, 'outgoing': False})
                            indicator_details[indicator]['devices'] = devices

                        indicators['indicators'].append(indicator_details)
            else:
                indicators = {'indicators':
                              {'incoming':
                                  {'count': len(incoming_indicators_list),
                                   'indicators': []
                                   },
                               'outgoing':
                                  {'count': len(outgoing_indicators_list),
                                   'indicators': []
                                   }
                               }
                              }

                for in_indicator in incoming_indicators_list:
                    indicator_devices = rpc_client.get_grouped_list(
                        url=self.INCOMING, message_type="incoming", message_key="deviceName", group_by=in_indicator)
                    in_indicator_detail = {}
                    devices = []

                    if in_indicator in outgoing_indicators_list:
                        in_indicator_detail[in_indicator] = {
                            'outgoing': True, 'count': indicator_devices[in_indicator]['count']}
                        outgoing_indicator_devices = rpc_client.get_grouped_list(
                            url=self.OUTGOING, message_type="outgoing", message_key="deviceName", group_by=in_indicator)

                        for device in indicator_devices[in_indicator]['list']:

                            if device in outgoing_indicator_devices['indicator'][list]:
                                devices.append(
                                    {'deviceName': device, 'outgoing': True})

                            else:
                                devices.append(
                                    {'deviceName': device, 'outgoing': True})

                    else:
                        in_indicator_detail[in_indicator] = {
                            'outgoing': False, 'count': indicator_devices[in_indicator]['count']}

                        for device in indicator_devices[in_indicator]['list']:
                            devices.append(
                                {'deviceName': device, 'outgoing': True})

                    in_indicator_detail[in_indicator]['devices'] = devices
                    indicators['indicators']['incoming']['indicators'].append(
                        in_indicator_detail)

                for out_indicator in outgoing_indicators_list:
                    indicator_devices = rpc_client.get_grouped_list(
                        url=self.OUTGOING, message_type="outgoing", message_key="indicatorName", group_by=out_indicator)
                    indicators['indicators']['outgoing']['indicators'].append({out_indicator: {
                                                                              'devices': indicator_devices[out_indicator]['list'], 'count': indicator_devices[out_indicator]['count']}})

            return indicators

        else:
            all_indicators = set()
            all_indicators.update(incoming_indicators_list)
            all_indicators.update(outgoing_indicators_list)
            indicator_details = {}
            devices = []

            if karg['indicator'] not in all_indicators:
                return indicator_details

            indicator = karg['indicator']

            if 'source' in karg:

                message_type = karg['source']
                url = self.INCOMING if karg['source'] == "incoming" else self.OUTGOING
                indicator_devices = rpc_client.get_grouped_list(
                    url=url, message_type=message_type, group_by=indicator, message_key="deviceName")

                if message_type == "outgoing":
                    if indicator not in outgoing_indicators_list:
                        return indicator_details
                    devices=[]
                    for device in indicator_devices[indicator]['list']:
                        devices.append({'deviceName':device,'outgoing':True})
                    indicator_details[indicator] = {
                        'count': indicator_devices[indicator]['count'], 'devices': devices,'outgoing':True}

                else:

                    if indicator not in incoming_indicators_list:
                        return indicator_details

                    if indicator in outgoing_indicators_list:
                        indicator_details[indicator] = {
                            'outgoing': True, 'count': indicator_devices[indicator]['count']}
                        indicator_outgoing_devices = rpc_client.get_grouped_list(
                            url=self.OUTGOING, message_type="outgoing", group_by=indicator, message_key="deviceName")

                        for device in indicator_devices[indicator]['list']:

                            if device in indicator_outgoing_devices[indicator]['list']:
                                devices.append(
                                    {'deviceName': device, 'outgoing': True})

                            else:
                                devices.append(
                                    {'deviceName': device, 'outgoing': False})

                    else:
                        indicator_details[indicator] = {
                            'outgoing': False, 'count': indicator_devices[indicator]['count']}

                        for device in indicator_devices[indicator]['list']:
                            devices.append(
                                {'deviceName': device, 'outgoing': False})

                    indicator_details[indicator]['devices'] = devices

            else:
                indicator_details = {}
                devices = []
                indicator_devices = rpc_client.get_grouped_list(
                    url=self.INCOMING, message_type="incoming", group_by=indicator, message_key="deviceName")
                indicator_outgoing_devices = rpc_client.get_grouped_list(
                    url=self.OUTGOING, message_type="outgoing", group_by=indicator, message_key="deviceName")

                if indicator in outgoing_indicators_list:
                    indicator_details[indicator] = {
                        'outgoing': True, 'count': indicator_devices[indicator]['count']}

                    for device in indicator_devices[indicator]['list']:

                        if device in indicator_outgoing_devices[indicator]['list']:
                            devices.append(
                                {'deviceName': device, 'outgoing': True})

                        else:
                            devices.append(
                                {'deviceName': device, 'outgoing': False})

                else:
                    indicator_details[indicator] = {
                        'outgoing': False, 'count': indicator_devices[indicator]['count']}
                    for device in indicator_devices[indicator]['list']:
                        devices.append(
                            {'deviceName': indicator, 'outgoing': True})
                indicator_details[indicator]['devices'] = devices
            return indicator_details

    def update_filter(self, **karg):
        kafka_publish = KafkaPublisher()
        rpc_client = KafkaClient()
        topic = app.config.get('KAFKA_FILTER_TOPIC')

        if 'device' not in karg and 'indicator' not in karg:
            raise Exception('Invalid method call')

        if 'action' not in karg:
            raise Exception('Invalid method call')
        elif karg['action'] not in ['enable', 'disable']:
            raise Exception('Invalid method call')

        if 'device' not in karg:
            devices = rpc_client.get_list(
                url=self.INCOMING, message_type="incoming", message_key="deviceName")
            indicators = [karg['indicator']]

        else:
            devices = [str(karg['device'])]
             
            incoming = rpc_client.get_grouped_list(
                url=self.INCOMING, message_type="incoming", group_by=karg['device'],message_key="indicatorName")[karg['device']]['list']
            outgoing   = rpc_client.get_grouped_list(
                url=self.OUTGOING, message_type="outgoing", group_by=karg['device'],message_key="indicatorName")[karg['device']]['list']
            indicators = incoming + outgoing

        if 'indicator' not in karg:
            devices = [str(karg['device'])]            
        else:
            indicators = [str(karg['indicator'])]

        for device in devices:

            for indicator in indicators:
                message = {"deviceName": device, "indicatorName": indicator, "enable": True} \
                    if karg['action'] == "enable" \
                    else {"deviceName": device, "indicatorName": indicator, "enable": False}
                key = device+indicator
                kafka_publish.publish_message(
                    topic, key=str(key), message=message)

