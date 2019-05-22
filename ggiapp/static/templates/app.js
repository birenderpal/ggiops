import { MDCTopAppBar } from "@material/top-app-bar";
import { MDCTextField } from '@material/textfield';
import { MDCTextFieldHelperText } from '@material/textfield/helper-text';
import { MDCSwitch } from '@material/switch';
import { MDCRipple } from '@material/ripple';
import {MDCList} from '@material/list';
import {MDCSnackbar} from '@material/snackbar';

import classNames from 'classnames';

const homeButton = new MDCRipple(document.querySelector('.mdc-icon-button'));

homeButton.unbounded = true;

const list = new MDCList(document.querySelector('.mdc-list'));
const buttonRipple = new MDCRipple(document.querySelector('.mdc-button'));
const searchHelperText = new MDCTextFieldHelperText(document.querySelector('.mdc-text-field-helper-text'));
const topAppBar = new MDCTopAppBar(document.querySelector('.mdc-top-app-bar'));


const searchTextField = new MDCTextField(document.querySelector('.mdc-text-field'));

const linkContent = document.getElementById('link-content')
const manageItem=document.querySelector('.manage-items') 

linkContent.style.display = "none";

/*
    Get all templates here
*/

var searchTemplate = document.getElementById('search-result').innerHTML
var manageTemplate = document.getElementById('manage-item').innerHTML
var snackResponse = document.getElementById('snackresponse').innerHTML
const searchableList = document.querySelectorAll('.searchresultlist')

const linkButtons = document.querySelectorAll('.link-button');

const linkClicked = (e) => {
    document.getElementById('result-list').innerHTML = "";
    linkContent.style.display = ""
    console.log(e.srcElement.innerHTML)
    document.getElementById('search').value = ""
    manageItem.innerHTML=""
    manageItem.style.display="none"
    var source = e.srcElement.innerHTML;
    source = source.trim()
    document.querySelector('.mdc-text-field-helper-text').innerHTML = source;
    var list
    fetch(`/api/${source}/devices`)
        .then(response => { return response.json() })
        .then(json => {
            var list = []
            json.devices.forEach(device => {
                list.push({ 'name': Object.keys(device).toString(), 'type': 'device' })
            })
            var listHTML = ""
            list.forEach(elem => {
                listHTML += searchTemplate.replace(/%%name%%/g, elem.name)
                    .replace(/%%source%%/g,source)
                    .replace(/%%type%%/g, elem.type)
            })
            document.getElementById('result-list').innerHTML = listHTML
        })
    fetch(`/api/${source}/indicators`)
        .then(response => { return response.json() })
        .then(json => {
            var list = []
            json.indicators.forEach(indicator => {
                list.push({ 'name': Object.keys(indicator).toString(), 'type': 'indicator' })
            })
            var listHTML = ""
            list.forEach(elem => {
                listHTML += searchTemplate.replace(/%%name%%/g, elem.name)
                    .replace(/%%source%%/g,source)
                    .replace(/%%type%%/g, elem.type)
            })
            document.getElementById('result-list').insertAdjacentHTML('beforeend',listHTML)
        })
}
const searchEvent = (e) => {
    var regex = new RegExp(e.srcElement.value, "i");
    var listItems = document.querySelectorAll('.item-name');
    manageItem.innerHTML="";
    manageItem.style.display="none";
    if (e.srcElement.value.length >=1){
        var listItems = document.querySelectorAll('.item-name');
        document.getElementById('result').hidden=false
        listItems.forEach(item => {
            if (item.innerHTML.search(regex) != -1) {

                item.closest('li').style.display = ""
            }
            else {
                item.closest('li').style.display = "none"
            }
        })    
    }
    else{
        document.getElementById('result').hidden=true
    }
}


const clickedResult = (e) =>{
    document.getElementById('result').hidden=true    
    var name = document.querySelectorAll('.item-name')[e.detail.index].innerText
    var type = document.querySelectorAll('.item-type')[e.detail.index].innerText
    var source = document.querySelectorAll('.searchresultlist')[e.detail.index].getAttribute('data-source')
    fetch(`/api/${source}/${type}/${name}`)
    .then(response=>{return response.json()})
    .then(json=>{
        var manageHTML = ""
        //var switchclass = className({""})
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
                                    .replace(/%%url%%/g,`${type}/${Object.keys(json).toString()}`)
        Object.values(details)[0].forEach(item=>{
                    var name=Object.assign({},item)
                    delete name.outgoing                                        
                    manageHTML += manageTemplate.replace(/%%switchclass%%/g,classNames('mdc-switch',{'mdc-switch--checked':item.outgoing}))
                                                .replace(/%%typoclass%%/g,classNames('mdc-typography--subtitle1'))
                                                .replace(/%%switch%%/g,classNames({'enabled' : item.outgoing,'disabled':!item.outgoing}))
                                                .replace(/%%name%%/g,Object.values(name).toString())
                                                .replace(/%%switchstatus%%/g,classNames({'checked':item.outgoing}))
                                                .replace(/%%url%%/g,`${type}/${Object.keys(json).toString()}/${secondType}/${Object.values(name).toString()}`)
                })
        manageItem.innerHTML = manageHTML
        manageItem.children[0].appendChild(span)
        manageItem.style.display=""
        const mdcSwitches = document.querySelectorAll('.mdc-switch')
        mdcSwitches.forEach( sw =>{
            MDCSwitch.attachTo(sw)
            sw.addEventListener('change',toggleSwitch)
        })
        
    })
}

list.listen('MDCList:action',clickedResult)

const searchInput = document.getElementById('search');
searchInput.addEventListener('keyup', searchEvent);

const toggleSwitch = (e) => {
    e.srcElement.labels[0].innerText = 
    classNames({"enabled":(e.srcElement.labels[0].innerText =="disabled"),
                "disabled":(e.srcElement.labels[0].innerText =="enabled"),
                "All":(e.srcElement.labels[0].innerText =="None"),
                "None":(e.srcElement.labels[0].innerText =="All")})
    if (e.srcElement.labels[0].innerText == "All"){
        console.log("Here in All")
        document.querySelectorAll('.mdc-switch').forEach(sw=>{
            var mdswitch = MDCSwitch.attachTo(sw)
            mdswitch.checked = true
            var labelText = mdswitch.root_.nextElementSibling.innerText
            mdswitch.root_.nextElementSibling.innerText = 
            classNames({"enabled":(labelText == "disabled")||(labelText =="enabled"),
                         "All":(labelText == "All")||(labelText =="None")})
           /* sw.addEventListener('change',(e)=>{
                e.preventDefault();
            })*/
        })
    }
    if (e.srcElement.labels[0].innerText == "None"){
        console.log("Here in None")
        var switches = document.querySelectorAll('.mdc-switch')
        switches.forEach(sw=>{
            var mdswitch = MDCSwitch.attachTo(sw)
            mdswitch.checked = false
            var labelText = mdswitch.root_.nextElementSibling.innerText
            //console.log(labelText)
            //console.log(classNames({"disabled":(labelText == "enabled"),
            //"None":(labelText == "None")}))
            mdswitch.root_.nextElementSibling.innerText = 
            classNames({"disabled":(labelText == "enabled")||(labelText =="disabled"),
                        "None":(labelText == "None")||(labelText =="All")})

        })
    }
    var type = e.srcElement.checked ? "POST":"DELETE"
    var url = e.srcElement.labels[0].getAttribute('data-url');
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) { 
            var jsonRes = JSON.parse(xhttp.responseText)                     
            if (jsonRes.status != "success"){
                var div = document.createElement('div')
                div.innerHTML = snackResponse.replace(/%%statusmessage%%/g,jsonRes.status)
                document.getElementById('main-content').appendChild(div)
                const snackbar = new MDCSnackbar(document.querySelector('.mdc-snackbar'));
                snackbar.open();
            }
            console.log(xhttp.responseText)
        }
      };
      xhttp.open(type, "/api/outgoing/"+url, true);
      xhttp.send();    
}

document.querySelector('.home').addEventListener('click', () => {
    linkContent.style.display = "none";
});
/*
document.querySelectorAll('.mdc-switch__native-control').forEach(sw =>{
    let swFnd= new MDCSwitch(sw)
    swFnd.listen('change',toggleSwitch)
    //swFnd.listen('MDCSwitchFoundation:change',toggleSwitch)
    //sw.addEventListener('MDCSwitchFoundation:change',toggleSwitch)
})
*/
linkButtons.forEach(linkButton => {
    linkButton.addEventListener('click', linkClicked);
});
