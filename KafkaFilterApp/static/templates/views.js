import {MDCSnackbar} from '@material/snackbar';
import {MDCSwitch} from '@material/switch';
import {MDCDialog} from '@material/dialog';
import classNames from 'classnames';

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
                listSearchItems.push({ 'name': Object.keys(device).toString(), 'type': 'device','source':source })
            })
        })
        fetch(`/api/${this.source}/indicators`)
        .then(response => { return response.json() })
        .then(json => {
            var list = []
            json.indicators.forEach(indicator => {
                listSearchItems.push({ 'name': Object.keys(indicator).toString(), 'type': 'indicator','source':source })
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
    init:()=>{
        linkContent.style.display="none";
        homePage.display.style="";
        manageItem.innerHTML=""
    },
    render:()=>{
        
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
                                        .replace(/%%switchclass%%/g,classNames('mdc-switch',{'mdc-switch--checked':Object.values(json)[0].outgoing}))
                                        .replace(/%%switch%%/g,classNames({'All' : Object.values(json)[0].outgoing,"None":!Object.values(json)[0].outgoing}))
                                        .replace(/%%switchstatus%%/g,classNames({'checked':Object.values(json)[0].outgoing}))
                                        .replace(/%%url%%/g,`${this.type}/${Object.keys(json).toString()}`)
            Object.values(details)[0].forEach(item=>{
                        var name=Object.assign({},item)
                        delete name.outgoing                                        
                        manageHTML += manageTemplate.replace(/%%switchclass%%/g,classNames('mdc-switch',{'mdc-switch--checked':item.outgoing}))
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

export var login={
    init:function(){
        this.logindialog = new MDCDialog(document.querySelector('.mdc-dialog'))
        
    },
    render:function(){        
        this.logindialog.open();
        document.getElementById('login').addEventListener('click',(e)=>{
            var username=document.getElementById('username').value
            var password=document.getElementById('password').value   
            var xhttp = new XMLHttpRequest();
        })
    },
}