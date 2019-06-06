import {MDCSnackbar} from '@material/snackbar';
import {MDCSwitch} from '@material/switch';
import {MDCDialog} from '@material/dialog';
import classNames from 'classnames';
import { MDCTextField } from '@material/textfield';
import * as d3 from "d3";

//
//    Get all templates here
//
var searchTemplate = document.getElementById('search-result').innerHTML
var manageTemplate = document.getElementById('manage-item').innerHTML
var homePage = document.getElementById('home').innerHTML
var snackResponse = document.getElementById('snackresponse').innerHTML
const manageItem=document.querySelector('.manage-items') 
const linkContent = document.getElementById('link-content');
// all templates above

export const AJAX = (url, action, callback) => {
    var xhttp = new XMLHttpRequest();
    xhttp.open(action, url, true);
    xhttp.send();
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            callback(xhttp.responseText)
        }
    };

}

export var snackbar = {  
    render:(jsonRes)=>{
        if (jsonRes.status != "success"){
            var div = document.createElement('div')
            div.innerHTML = snackResponse.replace(/%%statusmessage%%/g,jsonRes.status)
            document.getElementById('main-content').appendChild(div)
            const snackbar = new MDCSnackbar(document.querySelector('.mdc-snackbar'));
            snackbar.open();
        }
    }
}

export var search = {
    init:()=>{
        document.getElementById('result').hidden=false        

    },
    reset:()=>{
        manageItem.innerHTML="";
        manageItem.style.display="none";    
        document.getElementById('result-list').innerHTML = "";
        document.getElementById('result').hidden=true
    },
    render:(matched)=>{
        var listHTML = ""
        matched.forEach(elem => {
            listHTML += searchTemplate.replace(/%%name%%/g, elem.name)
                .replace(/%%source%%/g,elem.source)
                .replace(/%%type%%/g, elem.type)
        })
        document.getElementById('result-list').innerHTML = listHTML;

    }
}

export var links = {
    init:function(source){
        this.source=source;
        var listSearchItems=[]
        fetch(`/api/${this.source}/devices`)
        .then(response => { return response.json() })
        .then(json => {
            json.devices.forEach(device => {
                listSearchItems.push({ 'name': device, 'type': 'device','source':source })
            })
        })
        fetch(`/api/${this.source}/indicators`)
        .then(response => { return response.json() })
        .then(json => {
            var list = []
            json.indicators.forEach(indicator => {
                listSearchItems.push({ 'name': indicator, 'type': 'indicator','source':source })
            })
        })
        return listSearchItems

    },
    render:function(){
        document.getElementById('result-list').innerHTML = "";
        linkContent.style.display = "";
        document.getElementById('search').value = "";
        manageItem.innerHTML="";
        manageItem.style.display="none";              
        document.querySelector('.mdc-text-field-helper-text').innerHTML = this.source;    
    },
    reset:()=>{

    }
}

export var home ={    
    init:function(){
        linkContent.style.display="none";
        //homePage.display.style="";
        manageItem.innerHTML=""        
    },
    render:function(){
        var height=360;
        var width=360;
        var padding = 10;
 
        var svg1=d3.select("#svg1").append("svg")
        svg1.attr("width",width)
        svg1.attr("height",height)
        var svg2=d3.select("#svg2").append("svg")
        svg2.attr("width",width)
        svg2.attr("height",height)
        fetch("/api/devices")
        .then(response=>{return response.json()})
        .then((res)=>{   
            var dataset=[["incoming",res.devices.incoming.length],["outgoing",res.devices.outgoing.length]]
            var scale = d3.scaleLinear()
            scale.domain([0,d3.max(dataset,(d)=>d[1])])
            scale.range([0,height - padding])
            svg1.selectAll("rect")
            .data(dataset)
            .enter()
            .append("rect")
            .attr("x",(d,i)=>{return i*30})
            .attr("y",(d,i)=>{return height - scale(d[1]) - padding})
            .attr("height",(d,i)=>{return scale(d[1])})
            .attr("width",25)
            .attr("fill","teal")
            .attr("class","bar")
            .append("title")
            .text((d)=>{return d[0]})
            svg1.selectAll("text")
            .data(dataset)
            .enter()
            .append("text")
            .attr("x",(d,i)=>{return i*50})
            .attr("y",(d,i)=>{return height - scale(d[1]) - padding -3})
            .text((d)=>d[1])        
        })
        fetch("/api/indicators")
        .then(response=>{return response.json()})
        .then((res)=>{
            var dataset=[["incoming",res.indicators.incoming.length],["outgoing",res.indicators.outgoing.length]]
            var scale = d3.scaleLinear()
            scale.domain([0,d3.max(dataset,(d)=>d[1])])
            scale.range([0,height - padding])
            svg2.selectAll("rect")
            .data(dataset)
            .enter()
            .append("rect")
            .attr("x",(d,i)=>{return i*30})
            .attr("y",(d,i)=>{return height - scale(d[1]) - padding})
            .attr("height",(d,i)=>{return scale(d[1])})
            .attr("width",25)
            .attr("fill","teal")
            .attr("class","bar")
            .append("title")
            .text((d)=>{return d[0]})
            svg2.selectAll("text")
            .data(dataset)
            .enter()
            .append("text")
            .attr("x",(d,i)=>{return i*50})
            .attr("y",(d,i)=>{return height - scale(d[1]) - padding -3})
            .text((d)=>d[1])            
        })

        
        }
    }

const toggleSwitch = (e) => {
    e.srcElement.labels[0].innerText =
        classNames({
            "enabled": (e.srcElement.labels[0].innerText == "disabled"),
            "disabled": (e.srcElement.labels[0].innerText == "enabled"),
            "All": (e.srcElement.labels[0].innerText == "None"),
            "None": (e.srcElement.labels[0].innerText == "All")
        })
    if (e.srcElement.labels[0].innerText == "All") {
        document.querySelectorAll('.mdc-switch').forEach(sw => {
            var mdswitch = MDCSwitch.attachTo(sw)
            mdswitch.checked = true
            var labelText = mdswitch.root_.nextElementSibling.innerText
            mdswitch.root_.nextElementSibling.innerText =
                classNames({
                    "enabled": (labelText == "disabled") || (labelText == "enabled"),
                    "All": (labelText == "All") || (labelText == "None")
                })
        })
    }
    if (e.srcElement.labels[0].innerText == "None") {
        var switches = document.querySelectorAll('.mdc-switch')
        switches.forEach(sw => {
            var mdswitch = MDCSwitch.attachTo(sw)
            mdswitch.checked = false
            var labelText = mdswitch.root_.nextElementSibling.innerText
            mdswitch.root_.nextElementSibling.innerText =
                classNames({
                    "disabled": (labelText == "enabled") || (labelText == "disabled"),
                    "None": (labelText == "None") || (labelText == "All")
                })

        })
    }
    var type = e.srcElement.checked ? "POST" : "DELETE"
    var url = e.srcElement.labels[0].getAttribute('data-url');
    AJAX("/api/outgoing/" + url, type, (res) => {
        snackbar.render(JSON.parse(res))
    })
}

export var manage ={    
    init: function(source,type,name){
            document.getElementById('result').hidden=true
            this.source=source
            this.type=type
            this.name=name
            fetch('/authenticate')
            .then(response=>{return response.json()})
            .then(res=>{
                this.authenticated = res.authenticated
            })
    },
    render:function(){
        fetch(`/api/${this.source}/${this.type}/${this.name}`)
        .then(response=>{return response.json()})
        .then(json=>{
            var manageHTML = ""
            var details = Object.assign({},Object.values(json)[0])
            delete details.count
            delete details.outgoing
            const span = document.createElement('span');
            span.classList.add('mdc-typography--overline')
            span.innerText = Object.keys(details).toString();
            var secondType = Object.keys(details).toString().substr(0,Object.keys(details).toString().length -1);
            manageHTML += manageTemplate.replace(/%%name%%/g,Object.keys(json).toString())
                                        .replace(/%%typoclass%%/g,classNames('mdc-typography--headline6'))
                                        .replace(/%%switchclass%%/g,classNames('mdc-switch',{'mdc-switch--checked':Object.values(json)[0].outgoing},{'mdc-switch--disabled':!this.authenticated}))
                                        .replace(/%%switch%%/g,classNames({'All' : Object.values(json)[0].outgoing,"None":!Object.values(json)[0].outgoing}))
                                        .replace(/%%switchstatus%%/g,classNames({'checked':Object.values(json)[0].outgoing}))
                                        .replace(/%%url%%/g,`${this.type}/${Object.keys(json).toString()}`)
            Object.values(details)[0].forEach(item=>{
                        var name=Object.assign({},item)
                        delete name.outgoing                                        
                        manageHTML += manageTemplate.replace(/%%switchclass%%/g,classNames('mdc-switch',{'mdc-switch--checked':item.outgoing},{'mdc-switch--disabled':!this.authenticated}))
                                                    .replace(/%%typoclass%%/g,classNames('mdc-typography--subtitle1'))
                                                    .replace(/%%switch%%/g,classNames({'enabled' : item.outgoing,'disabled':!item.outgoing}))
                                                    .replace(/%%name%%/g,Object.values(name).toString())
                                                    .replace(/%%switchstatus%%/g,classNames({'checked':item.outgoing}))
                                                    .replace(/%%url%%/g,`${this.type}/${Object.keys(json).toString()}/${secondType}/${Object.values(name).toString()}`)
                    })
            manageItem.innerHTML = manageHTML
            manageItem.children[0].appendChild(span)
            manageItem.style.display=""  
            var mdcSwitches=document.querySelectorAll('.mdc-switch')
            mdcSwitches.forEach(sw => {
                MDCSwitch.attachTo(sw)
                sw.addEventListener('change', toggleSwitch)
            })    
        })
    }
}

export var register={
    render:function(){        
        this.registerElem = document.getElementById('register-dialog')
        this.register = MDCDialog.attachTo(this.registerElem)
        this.register.open();

        document.getElementById('register').addEventListener('click',(e)=>{
            var username=document.getElementById('rusername').value
            var password=document.getElementById('rpassword').value   
            var email=document.getElementById('remail').value
            var requestData ={'username':username,'password':password,'email':email}
            var xhttp = new XMLHttpRequest();
            xhttp.open("POST","/register",true)
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");            
            xhttp.send(JSON.stringify(requestData));
            var register = this.register
            xhttp.onreadystatechange =function(){
                if (this.readyState == 4 && this.status == 200) {
                    console.log(this.responseText)
                    var res = JSON.parse(this.responseText)
                    if (res.status == "success"){
                        register.close();
                    }                    
                    else{
                        document.getElementById('message').innerText=res.status                        
                    }
                }
            }
        })
    }
}
export var login={
    init:function(){
        this.logindialogElem = document.getElementById('login-dialog')
        this.logindialog = MDCDialog.attachTo(this.logindialogElem)        
        var userFieldElem = document.getElementById('username-field')
        this.userField = MDCTextField.attachTo(userFieldElem)
        this.logindialog.layout(this.userField)
        document.getElementById('username').value=""
        document.getElementById('password').value=""
    },
    render:function(){
        var xhttp = new XMLHttpRequest();
        fetch('/authenticate')
        .then(response=>{return response.json()})
        .then(res=>{
            if (res.authenticated){
                xhttp.open("POST","/logout",true)                
                xhttp.send();  
                this.action="logout"
                document.getElementById('logged-user').innerText=""
                this.logindialog.close()
            }
            else{
                this.action="login"
                this.logindialog.open();
            }
        }) 
        document.getElementById('login').addEventListener('click',(e)=>{
            var username=document.getElementById('username').value
            var password=document.getElementById('password').value   
            var requestData ={'username':username,'password':password}

            if (this.action=="login"){   
                xhttp.open("POST","/login",true)
                xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");            
                xhttp.send(JSON.stringify(requestData));
                var logindialog = this.logindialog
                xhttp.onreadystatechange =function(){
                    if (this.readyState == 4 && this.status == 200) {
                        var res = JSON.parse(this.responseText)    
                        if (res.status == "register"){
                            logindialog.close()
                            register.render()
                        }
                        else if (res.status == "success"){
                            document.getElementById('logged-user').innerText=`loged as ${username}`
                            logindialog.close();
                        } 
                        else{
                            var loginMsgElem = document.getElementById('login-message')
                            logindialog.layout(loginMsgElem)
                            loginMsgElem.innerText=res.status
                        }                   
                    }
                }
            }
        })
    },
}