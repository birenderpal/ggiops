'''
Created on 23/04/2018

@author: t821012
'''
from ggiapp import app
import datetime
import json
import httplib2
import urllib
import sys
import codecs
from flask import Flask, jsonify, request
from ggiapp.controllers import SplunkApp
HOSTNAME="localhost:8000"
@app.route('/api/splunk/indicators')
def get_all_indicators():
    if request.method == 'GET':
        splunkapp = SplunkApp.SplunkApp(HOSTNAME)
        return jsonify({"indicators":splunkapp.get_splunk_indicators()})
@app.route('/api/splunk/devices')
def get_devices():
    if request.method == 'GET':        
        splunkapp = SplunkApp.SplunkApp(HOSTNAME)                
        return jsonify({"devices":splunkapp.get_splunk_devices()})

@app.route('/api/splunk/indicator/<string:indicator>',methods=['GET','PUT','DELETE'])
def get_indicators(indicator):
    if request.method == 'GET':
        splunkapp = SplunkApp.SplunkApp(HOSTNAME)        
        return jsonify(splunkapp.get_splunk_indicator(indicator))
    if request.method == 'PUT':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.enable_indicator(indicator)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})    
    if request.method == 'DELETE':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.disable_indicator(indicator=indicator)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})   
@app.route('/api/splunk/indicator/<string:indicator>/device/<string:device>',methods=['POST','DELETE'])
def enable_indicator_dev(device,indicator):
    if request.method == 'POST':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.enable_indicator(indicator=indicator,device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
    if request.method == 'DELETE':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.disable_indicator(indicator=indicator,device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})                 

""" @app.route('/api/splunk/indicator/<string:indicator>/enable')
def enable_indicator(indicator):
    if request.method == 'GET':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.enable_indicator(indicator)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})         

@app.route('/api/splunk/indicator/<string:indicator>/disable')
def disable_indicator(indicator):
    if request.method == 'GET':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.disable_indicator(indicator=indicator)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
"""
@app.route('/api/splunk/device/<string:device>',methods=['GET','POST','PUT','DELETE'])
def get_device(device):
    if request.method == 'GET':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        #splunkapp.get_splunk_device_metrics(device)
        return jsonify(splunkapp.get_splunk_device(device))
    if request.method == 'POST':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)        
        try:
            splunkapp.enable_indicator(device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
    if request.method == 'DELETE':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.disable_indicator(device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
            
@app.route('/api/splunk/device/<string:device>/indicator/<string:indicator>',methods=['POST','DELETE'])
def enable_dev_indicator(device,indicator):
    if request.method == 'POST':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.enable_indicator(indicator=indicator,device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})
    if request.method == 'DELETE':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        try:
            splunkapp.disable_indicator(indicator=indicator,device=device)
            return jsonify({"status":"success"})
        except Exception as ex:
            return jsonify({"status":str(ex)})


@app.route('/api/sevone/devices')
def get_sevone_devices():
    if request.method == 'GET':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        return jsonify({"devices":splunkapp.get_sevone_devices()})

@app.route('/api/sevone/device/<string:device>')
def get_sevone_device_indicators(device):
    if request.method == 'GET':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        return jsonify(splunkapp.get_sevone_device(device))

@app.route('/api/sevone/indicators')
def get_all_sevone_indicators():
    if request.method == 'GET':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        return jsonify({"indicators":splunkapp.get_sevone_indicators()})

@app.route('/api/sevone/indicator/<string:indicator>')
def get_sevone_indicator(indicator):
    if request.method == 'GET':
        splunkapp=SplunkApp.SplunkApp(HOSTNAME)
        return jsonify(splunkapp.get_sevone_indicator(indicator))
