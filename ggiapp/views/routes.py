from ggiapp import app
from flask import jsonify, request,json, render_template,redirect
from ggiapp.controllers.SplunkApp import SplunkApp
#===============================================================================
# logging.config.fileConfig('logging.conf')
# LOGGER = logging.getLogger('splunk_query')
#===============================================================================


HOSTNAME="localhost:8000"

@app.route('/')

def index():
    splunkapp = SplunkApp(HOSTNAME)
    sp_devices = splunkapp.get_splunk_devices()    
    sp_indicators = splunkapp.get_splunk_indicators()
    s1_devices = splunkapp.get_sevone_devices()
    s1_indicators = splunkapp.get_sevone_indicators()
    return render_template('index.html',sp_devices=sp_devices,sp_indicators=sp_indicators,s1_devices=s1_devices,s1_indicators=s1_indicators)

@app.route('/splunk',methods = ['GET','POST'])
def splunk():
    splunkapp = SplunkApp(HOSTNAME)
    devices = splunkapp.get_splunk_devices()
    indicators = splunkapp.get_splunk_indicators()
    if request.method == 'GET':       
        type=request.args.get('type', '') 
        if type:
            return render_template('details.html',type=type,devices=devices,indicators=indicators)    
        else:
            return render_template('info.html',type="splunk",devices=devices,indicators=indicators)    
    if request.method == 'POST':
        print("post received")        
        device_details=request.args.get('devices', '')
        print(device_details[0])
        return render_template('info.html',devices=device_details)
@app.route('/splunk/devicedetails',methods = ['GET','POST'])
def splunk_device_details():
    splunkapp = SplunkApp(HOSTNAME)
    device_list=[]
    devices = splunkapp.get_splunk_devices()
    for device in devices:                
        device_details={'deviceName':device,'count':len(splunkapp.get_splunk_device(device)[device]['indicators']),'indicators':splunkapp.get_splunk_device(device)[device]['indicators'],'sevoneCount':len(splunkapp.get_sevone_device(device)[device]['indicators'])}
        device_list.append(device_details)
    indicators = splunkapp.get_splunk_indicators()
    if request.method == 'GET':       
        return jsonify(device_list)
    if request.method == 'POST':
        return jsonify(device_list)

@app.route('/splunk/indicatordetails',methods = ['GET'])
def splunk_indicator_details():
    splunkapp = SplunkApp(HOSTNAME)
    indicator_list=[]
    indicators = splunkapp.get_splunk_indicators()
    for indicator in indicators:            
        print(splunkapp.get_sevone_indicator(indicator)[indicator])    
        indicator_details={'indicatorName':indicator,'count':len(splunkapp.get_splunk_indicator(indicator)[indicator]['devices']),'splunkDevices':splunkapp.get_splunk_indicator(indicator)[indicator]['devices'],'sevoneCount':len(splunkapp.get_sevone_indicator(indicator)[indicator]['devices']),'sevoneDevices':splunkapp.get_sevone_indicator(indicator)[indicator]['devices']}
        indicator_list.append(indicator_details)    
    if request.method == 'GET':       
        return jsonify(indicator_list)
    if request.method == 'POST':
        return jsonify(indicator_list)

@app.route('/sevone/devicedetails',methods = ['GET','POST'])
def sevone_device_details():
    splunkapp = SplunkApp(HOSTNAME)
    device_list=[]
    devices = splunkapp.get_sevone_devices()        
    for device in devices:                
        
        if not (splunkapp.get_splunk_device(device)[device]['indicators']):
            count=0            
        else:
            count=len(splunkapp.get_splunk_device(device)[device]['indicators'])            
        device_details={'deviceName':device,'count':count,'indicators':splunkapp.get_sevone_device(device)[device]['indicators'],'sevoneCount':len(splunkapp.get_sevone_device(device)[device]['indicators'])}        
        device_list.append(device_details)    
    if request.method == 'GET':       
        return jsonify(device_list)
    if request.method == 'POST':
        return jsonify(device_list)

@app.route('/sevone/indicatordetails',methods = ['GET'])
def sevone_indicator_details():
    splunkapp = SplunkApp(HOSTNAME)
    indicator_list=[]
    indicators = splunkapp.get_sevone_indicators()
    for indicator in indicators:      
        if indicator in splunkapp.get_splunk_indicator(indicator):
            count=len(splunkapp.get_splunk_indicator(indicator)[indicator]['devices'])
            splunk_devices=splunkapp.get_splunk_indicator(indicator)[indicator]['devices']
        else:
            count=0
            splunk_devices=["None"]
        indicator_details={'indicatorName':indicator,'count':count,'splunkDevices':splunk_devices,'sevoneCount':len(splunkapp.get_sevone_indicator(indicator)[indicator]['devices']),'sevoneDevices':splunkapp.get_sevone_indicator(indicator)[indicator]['devices']}
        indicator_list.append(indicator_details)    
    if request.method == 'GET':       
        return jsonify(indicator_list)
    if request.method == 'POST':
        return jsonify(indicator_list)


@app.route('/sevone')
def sevone():
    splunkapp = SplunkApp(HOSTNAME)
    devices = splunkapp.get_sevone_devices()
    indicators = splunkapp.get_sevone_indicators()
    return render_template('info.html',type="sevone",devices=devices,indicators=indicators)    
@app.route('/customer/add',methods=['GET','POST','DELETE'])

def new_customer():
    if request.method == 'GET':
        return render_template("add_customer.html")
    if request.method =='POST':
        customer_info = request.form.get('customer_info','')
        cust_code = request.form.get('custcode','')            
        domain = request.form.get('domain','')
        hostname = request.form.get('hostname','')
        cust_data={'customer_info':customer_info,'cust_code':cust_code}
        smarts_data={'domain':domain,'hostname':hostname}
        customerUpdate=db.customer.update_one({'cust_code':cust_code},{'$set':cust_data},upsert=True)
        smartsUpdate=db.smarts_server.update_one({'domain':domain},{'$set':smarts_data},upsert=True)
        
        if customerUpdate.matched_count == 1:
            if customerUpdate.modified_count == 1:
                cust_status='CUST_UP'
            else:
                cust_status='CUST'                
        else:
            cust_status='CUST_INS'
    
        if smartsUpdate.matched_count == 1:
            if smartsUpdate.modified_count == 1:
                smarts_status='SM_UP'
            else:
                smarts_status='SM'
        else:
            smarts_status='SM_INS'
        return render_template('add_customer.html',cstatus=cust_status,smstatus=smarts_status)
        
@app.route('/device/<string:device>',methods=['GET','PUT','POST'])

def delete_device(device):
    dev = db.devices.find_one({'SystemName':device})
    smarts_info = dev['smarts_info']           
    if request.method == 'POST':
        smarts_api = SmartsAPI(smarts_info['hostname'],smarts_info['domain'])
        return_code = smarts_api.delete_device(device)          
        return jsonify(return_code)
    elif request.method == 'GET':        
        return render_template("device_info.html",device=dev)
