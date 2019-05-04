'''
Created on 23/04/2018

@author: Birender Pal
'''
from ggiapp import app
import datetime
import json
import httplib2
import urllib
from flask import Flask, jsonify, request
from flask_restful import Resource,Api
from flask_restful_swagger import swagger
from ggiapp.controllers import SplunkApp
HOSTNAME="localhost:8000"
#api = Api(app)
api = swagger.docs(Api(app),apiVersion='1',api_spec_url="/api/v1/docs",description="GGI app",basePath="/api")

class SplunkIndicators(Resource):   
    @swagger.operation(
        notes='get indicator details in splunk',
        summary='get enabled indicators',
        tags='splunk',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "indicators": "[all enabled indicators]"})
            }
          ]        
    )
    def get(self):
        splunkapp = SplunkApp.SplunkApp(HOSTNAME)
        return jsonify({"indicators":splunkapp.get_splunk_indicators()})
api.add_resource(SplunkIndicators,'/api/splunk/indicators')

class SplunkDevices(Resource):   
    @swagger.operation(
        notes='get device details in splunk',
        description='get device details in splunk',
        summary='get enabled devices',
        tags='splunk',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "devices": "[all enabled devices]"})
            }
          ]        
    )    
    def get(self):
        splunkapp = SplunkApp.SplunkApp(HOSTNAME)                
        return jsonify({"devices":splunkapp.get_splunk_devices()})
api.add_resource(SplunkDevices,'/api/splunk/devices')
class SplunkIndicator(Resource):
    @swagger.operation(
        notes='get indicator details in splunk',
        description='get indicator details in splunk',
        summary='get indicator',
        tags='splunk',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "indicator": {
                                "devices": "[devices indicator enabled on]"
                            }
                        })
            }
          ]        
    )
    def get(self,indicator):        
        splunkapp = SplunkApp.SplunkApp(HOSTNAME)
        return jsonify(splunkapp.get_splunk_indicator(indicator))
    @swagger.operation(
        notes='enable indicator in splunk for all devices',
        tags='splunk',
        summary='enable indicator in splunk for all devices',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def post(self,indicator):        
        splunkapp = SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.enable_indicator(indicator)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})  
    @swagger.operation(
        notes='disable indicator in splunk for all devices',
        tags='splunk',
        summary='disable indicator in splunk for all devices',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def delete(self,indicator):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.disable_indicator(indicator=indicator)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})   

api.add_resource(SplunkIndicator,'/api/splunk/indicator/<string:indicator>')

class SplunkIndicatorDevice(Resource):
    @swagger.operation(
        notes='enable indicator in splunk for a device',
        tags='splunk',
        summary='enable indicator in splunk for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def post(self,indicator,device):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.enable_indicator(indicator=indicator,device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
    @swagger.operation(
        notes='disable indicator in splunk for a device',
        tags='splunk',
        summary='disable indicator in splunk for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def delete(self,indicator,device):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.disable_indicator(indicator=indicator,device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})                 
api.add_resource(SplunkIndicatorDevice,'/api/splunk/indicator/<string:indicator>/device/<string:device>')

class SplunkDevice(Resource):
    @swagger.operation(
        notes='get indicators in splunk for a device',
        tags='splunk',
        summary='get indicators in splunk for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def get(self,device):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)       
        return jsonify(splunkapp.get_splunk_device(device))
    @swagger.operation(
        notes='enable all indicators in splunk for a device',
        tags='splunk',
        summary='enable all indicators in splunk for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def post(self,device):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)        
        try:
            splunkapp.enable_indicator(device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
    @swagger.operation(
        notes='disable all indicators in splunk for a device',
        tags='splunk',
        summary='disable all indicators in splunk for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )            
    def delete(self,device):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.disable_indicator(device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
api.add_resource(SplunkDevice,'/api/splunk/device/<string:device>')

class SplunkDeviceIndicator(Resource):
    @swagger.operation(
        notes='enable indicator to splunk for a device',
        tags='splunk',
        summary='enable indicator to splunk for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def post(self,device):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)        
        try:
            splunkapp.enable_indicator(device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
    @swagger.operation(
        notes='disable indicator to splunk for a device',
        tags='splunk',
        summary='disable indicator to splunk for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )            
    def delete(self,device):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.disable_indicator(device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
api.add_resource(SplunkDeviceIndicator,'/api/splunk/device/<string:device>/indicator/<string:indictor>')

class SevOneIndicators(Resource):   
    @swagger.operation(
        notes='get all available indicators',
        summary='get available indicators',
        tags='sevone',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "indicators": "[all available indicators]"})
            }
          ]        
    )
    def get(self):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        return jsonify({"indicators":splunkapp.get_sevone_indicators()})
api.add_resource(SevOneIndicators,'/api/sevone/indicators')

class SevOneIndicator(Resource):   
    @swagger.operation(
        notes='get indicator details available in sevone',
        summary='get indicator detail',
        tags='sevone',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "{indicator}": "[list of devices with this indicator]"})
            }
          ]        
    )
    def get(self,indicator):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        return jsonify(splunkapp.get_sevone_indicator(indicator))
api.add_resource(SevOneIndicator,'/api/sevone/indicator/<string:indicator>')
class SevOneDevices(Resource):   
    @swagger.operation(
        notes='get all devices',
        summary='get all devices',
        tags='sevone',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "devices": "[all devices]"})
            }
          ]        
    )
    def get(self):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        return jsonify({"devices":splunkapp.get_sevone_devices()})
api.add_resource(SevOneDevices,'/api/sevone/devices')

class SevOneDevice(Resource):   
    @swagger.operation(
        notes='get device detail',
        summary='get device detail',
        tags='sevone',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "{device}": "[all indicators for this device]"})
            }
          ]        
    )
    def get(self,device):
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        return jsonify(splunkapp.get_sevone_device(device))
api.add_resource(SevOneDevice,'/api/sevone/device/<string:device>')