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
from ggiapp.controllers.GGIStream import GGIStream
#HOSTNAME="localhost:8000"
#api = Api(app)
api = swagger.docs(Api(app),apiVersion='1',api_spec_url="/api/v1/docs",description="GGI app",basePath="/api")


class Devices(Resource):
    @swagger.operation(
        notes='get indicator details in outgoing',
        summary='get enabled indicators',
        tags='outgoing',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "indicators": "[all enabled indicators]"})
            }
          ]        
    )
    def get(self):
        ggi_app = GGIStream()
        return ggi_app.get_devices()
api.add_resource(Devices,'/api/devices')


class DeviceDetails(Resource):
    @swagger.operation(
        notes='get indicator details in outgoing',
        summary='get enabled indicators',
        tags='outgoing',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "indicators": "[all enabled indicators]"})
            }
          ]        
    )
    def get(self,device):
        ggi_app = GGIStream()
        return ggi_app.get_devices(device=device)
api.add_resource(DeviceDetails,'/api/device/<string:device>')

class Indicators(Resource):
    @swagger.operation(
        notes='get indicator details in outgoing',
        summary='get enabled indicators',
        tags='outgoing',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "indicators": "[all enabled indicators]"})
            }
          ]        
    )
    def get(self):
        ggi_app = GGIStream()
        return jsonify(ggi_app.get_indicators())
api.add_resource(Indicators,'/api/indicators')

class IndicatorDetails(Resource):
    @swagger.operation(
        notes='get indicator details in outgoing',
        summary='get enabled indicators',
        tags='outgoing',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "indicators": "[all enabled indicators]"})
            }
          ]        
    )
    def get(self,indicator):
        ggi_app = GGIStream()
        return jsonify(ggi_app.get_indicators(indicator=indicator))
api.add_resource(IndicatorDetails,'/api/indicator/<string:indicator>')

class OutgoingIndicators(Resource):   
    @swagger.operation(
        notes='get indicator details in outgoing',
        summary='get enabled indicators',
        tags='outgoing',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "indicators": "[all enabled indicators]"})
            }
          ]        
    )
    def get(self):
        ggi_app = GGIStream()
        return jsonify(ggi_app.get_indicators(source="outgoing"))
api.add_resource(OutgoingIndicators,'/api/outgoing/indicators')

class OutgoingDevices(Resource):   
    @swagger.operation(
        notes='get device details in outgoing',
        description='get device details in outgoing',
        summary='get enabled devices',
        nickname='/outgoing/devices',
        tags='outgoing',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "devices": "[all enabled devices]"})
            }
          ]        
    )    
    def get(self):
        ggi_app = GGIStream()               
        return jsonify(ggi_app.get_devices(source="outgoing"))
api.add_resource(OutgoingDevices,'/api/outgoing/devices')
class OutgoingIndicator(Resource):
    @swagger.operation(
        notes='get indicator details in outgoing',
        description='get indicator details in outgoing',
        summary='get indicator',
        tags='outgoing',
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
        ggi_app=GGIStream()
        indicators=ggi_app.get_indicators()['indicators']['splunkIndicators']['indicators']
        indicator_detail=404
        for i in indicators:
            if indicator in i:
                indicator_detail={indicator:i[indicator]}
        return jsonify(indicator_detail)    
    @swagger.operation(
        notes='enable indicator in outgoing for all devices',
        tags='outgoing',
        summary='enable indicator in outgoing for all devices',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def post(self,indicator):        
        ggi_app = GGIStream()
        try:
            ggi_app.enable_indicator(indicator)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})  
    @swagger.operation(
        notes='disable indicator in outgoing for all devices',
        tags='outgoing',
        summary='disable indicator in outgoing for all devices',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def delete(self,indicator):
        ggi_app=GGIStream()
        try:
            ggi_app.disable_indicator(indicator=indicator)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})   
api.add_resource(OutgoingIndicator,'/api/outgoing/indicator/<string:indicator>')

class OutgoingIndicatorDevice(Resource):
    @swagger.operation(
        notes='enable indicator in outgoing for a device',
        tags='outgoing',
        summary='enable indicator in outgoing for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def post(self,indicator,device):
        ggi_app=GGIStream()
        try:
            ggi_app.enable_indicator(indicator=indicator,device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
    @swagger.operation(
        notes='disable indicator in outgoing for a device',
        tags='outgoing',
        summary='disable indicator in outgoing for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def delete(self,indicator,device):
        ggi_app=GGIStream()
        try:
            ggi_app.disable_indicator(indicator=indicator,device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})                 
api.add_resource(OutgoingIndicatorDevice,'/api/outgoing/indicator/<string:indicator>/device/<string:device>')

class OutgoingDevice(Resource):
    @swagger.operation(
        notes='get indicators in outgoing for a device',
        tags='outgoing',
        summary='get indicators in outgoing for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def get(self,device):
        ggi_app=GGIStream()
        return jsonify(ggi_app.get_devices(device=device,source="outgoing"))
        
    @swagger.operation(
        notes='enable all indicators in outgoing for a device',
        tags='outgoing',
        summary='enable all indicators in outgoing for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def post(self,device):
        ggi_app=GGIStream()        
        try:
            ggi_app.enable_indicator(device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
    @swagger.operation(
        notes='disable all indicators in outgoing for a device',
        tags='outgoing',
        summary='disable all indicators in outgoing for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )            
    def delete(self,device):
        ggi_app=GGIStream()
        try:
            ggi_app.disable_indicator(device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
api.add_resource(OutgoingDevice,'/api/outgoing/device/<string:device>')

class OutgoingDeviceIndicator(Resource):
    @swagger.operation(
        notes='enable indicator to outgoing for a device',
        tags='outgoing',
        summary='enable indicator to outgoing for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )
    def post(self,device,indicator):
        ggi_app=GGIStream()        
        try:
            ggi_app.enable_indicator(device=device,indicator=indicator)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
    @swagger.operation(
        notes='disable indicator to outgoing for a device',
        tags='outgoing',
        summary='disable indicator to outgoing for a device',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({"status":"success|error message"})
            }
          ]
    )            
    def delete(self,device,indicator):
        ggi_app=GGIStream()
        try:
            ggi_app.disable_indicator(device=device,indicator=indicator)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
api.add_resource(OutgoingDeviceIndicator,'/api/outgoing/device/<string:device>/indicator/<string:indicator>')

class IncomingIndicators(Resource):   
    @swagger.operation(
        notes='get all available indicators',
        summary='get available indicators',
        tags='incoming',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "indicators": "[all available indicators]"})
            }
          ]        
    )
    def get(self):
        ggi_app=GGIStream()
        return jsonify(ggi_app.get_indicators(source="incoming"))
api.add_resource(IncomingIndicators,'/api/incoming/indicators')

class IncomingIndicator(Resource):   
    @swagger.operation(
        notes='get indicator details available in incoming',
        summary='get indicator detail',
        tags='incoming',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "{indicator}": "[list of devices with this indicator]"})
            }
          ]        
    )
    def get(self,indicator):
        ggi_app=GGIStream()
        return jsonify(ggi_app.get_indicators(indicator=indicator,source="incoming"))
api.add_resource(IncomingIndicator,'/api/incoming/indicator/<string:indicator>')
class IncomingDevices(Resource):   
    @swagger.operation(
        notes='get all devices',
        summary='get all devices',
        tags='incoming',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "devices": "[all devices]"})
            }
          ]        
    )
    def get(self):
        ggi_app=GGIStream()
        return jsonify(ggi_app.get_devices(source="incoming"))
api.add_resource(IncomingDevices,'/api/incoming/devices')

class IncomingDevice(Resource):   
    @swagger.operation(
        notes='get device detail',
        summary='get device detail',
        tags='incoming',
        responseMessages=[
            {
              "code": 200,
              "message": json.dumps({
                            "{device}": "[all indicators for this device]"})
            }
          ]        
    )
    def get(self,device):
        ggi_app=GGIStream()
        return jsonify(ggi_app.get_devices(device=device,source="incoming"))
api.add_resource(IncomingDevice,'/api/incoming/device/<string:device>')