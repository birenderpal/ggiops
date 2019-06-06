'''
Created on 23/04/2018

@author: Birender Pal
'''
from KafkaFilterApp import app
import datetime
import json
import httplib2
import urllib
from flask import Flask, jsonify, request,abort
from flask_restplus import Resource,Api
from KafkaFilterApp.controllers.GGIStream import GGIStream
api = Api(app=app,doc="/api/docs",version=1.0,title="Filter Stream app")


class Source(Resource):
    def get(self,source):
        ggi_app = GGIStream()
        if source not in ["incoming","outgoing"]:
            abort(404,"Invalid source")
        devices= ggi_app.get_devices(source=source)
        indicators= ggi_app.get_indicators(source=source)
        return jsonify({source:[devices,indicators]})
api.add_resource(Source,'/api/<string:source>')

class Devices(Resource):
    def get(self):
        ggi_app = GGIStream()
        return ggi_app.get_devices()
api.add_resource(Devices,'/api/devices')


class DeviceDetails(Resource):
    def get(self,device):
        ggi_app = GGIStream()
        return ggi_app.get_devices(device=device)
api.add_resource(DeviceDetails,'/api/device/<string:device>')

class Indicators(Resource):
    def get(self):
        ggi_app = GGIStream()
        return jsonify(ggi_app.get_indicators())
api.add_resource(Indicators,'/api/indicators')

class IndicatorDetails(Resource):
    def get(self,indicator):
        ggi_app = GGIStream()
        return jsonify(ggi_app.get_indicators(indicator=indicator))
api.add_resource(IndicatorDetails,'/api/indicator/<string:indicator>')

class SourceIndicators(Resource):   
    def get(self,source):
        ggi_app = GGIStream()
        return jsonify(ggi_app.get_indicators(source=source))
api.add_resource(SourceIndicators,'/api/<string:source>/indicators')

class SourceDevices(Resource):   
    def get(self,source):
        ggi_app = GGIStream()               
        return jsonify(ggi_app.get_devices(source=source))
api.add_resource(SourceDevices,'/api/<string:source>/devices')
class SourceIndicator(Resource):
    def get(self,indicator,source):
        ggi_app=GGIStream()
        return jsonify(ggi_app.get_indicators(indicator=indicator,source=source))    

    def post(self,indicator,source):        
        ggi_app = GGIStream()
        try:
            ggi_app.update_filter(indicator=indicator,action="enable")            
        except Exception as ex:
            return jsonify({"status":str(ex)})  
        else:
            return jsonify({"status":"success"})
    def delete(self,indicator,source):
        ggi_app=GGIStream()
        try:
            ggi_app.update_filter(indicator=indicator,action="disable")
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})   
api.add_resource(SourceIndicator,'/api/<string:source>/indicator/<string:indicator>')

class UpdateIndicatorDevice(Resource):
    def post(self,indicator,device):
        ggi_app=GGIStream()
        try:
            ggi_app.update_filter(indicator=indicator,device=device,action="enable")
        except Exception as ex:
            return jsonify({"status":str(ex)})
        else:
            return jsonify({"status":"success"})

    def delete(self,indicator,device):
        ggi_app=GGIStream()
        try:
            ggi_app.update_filter(indicator=indicator,device=device,action="disable")
        except Exception as ex:
            return jsonify({"status":str(ex)})                 
        else:
            return jsonify({"status":"success"})

api.add_resource(UpdateIndicatorDevice,'/api/<string:source>/indicator/<string:indicator>/device/<string:device>')

class SourceDevice(Resource):
    def get(self,device,source):
        ggi_app=GGIStream()
        return jsonify(ggi_app.get_devices(device=device,source=source))
        
    def post(self,device,source):
        ggi_app=GGIStream()        
        try:
            ggi_app.update_filter(device=device,action="enable")
        except Exception as ex:
            return jsonify({"status":str(ex)})
        else:
            return jsonify({"status":"success"})

    def delete(self,device,source):
        ggi_app=GGIStream()
        try:
            ggi_app.update_filter(device=device,action="disable")
        except Exception as ex:
            return jsonify({"status":str(ex)})
        else:
            return jsonify({"status":"success"})

api.add_resource(SourceDevice,'/api/<string:source>/device/<string:device>')

class UpdateDeviceIndicator(Resource):
    def post(self,device,indicator):
        ggi_app=GGIStream()        
        try:
            ggi_app.update_filter(device=device,indicator=indicator,action="enable")
        except Exception as ex:
            return jsonify({"status":str(ex)})
        else:
            return jsonify({"status":"success"})
    def delete(self,device,indicator):
        ggi_app=GGIStream()
        try:
            ggi_app.update_filter(device=device,indicator=indicator,action="disable")
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
api.add_resource(UpdateDeviceIndicator,'/api/outgoing/device/<string:device>/indicator/<string:indicator>')