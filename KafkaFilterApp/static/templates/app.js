import { MDCTopAppBar } from "@material/top-app-bar";
import { MDCTextField } from '@material/textfield';
import { MDCTextFieldHelperText } from '@material/textfield/helper-text';
import { MDCRipple } from '@material/ripple';
import { MDCList } from '@material/list';
import {search, links, manage,login} from './views';

const list = new MDCList(document.querySelector('.mdc-list'));
const searchHelperText = new MDCTextFieldHelperText(document.querySelector('.mdc-text-field-helper-text'));
const topAppBar = new MDCTopAppBar(document.querySelector('.mdc-top-app-bar'));
const searchTextField = new MDCTextField(document.querySelector('.mdc-text-field'));
const linkContent = document.getElementById('link-content')
var listSearchItems = [];
linkContent.style.display = "none";



//
//Add ripples to all button 
//

document.querySelectorAll('.mdc-button').forEach(button => {
    MDCRipple.attachTo(button);
})

document.querySelectorAll('.mdc-icon-button').forEach(button => {
    MDCRipple.attachTo(button).unbounded = true;
})

window.onload=(e)=>{
    fetch('/authenticate')
    .then(response=>{return response.json()})
    .then(res=>{
        if (res.authenticated){
            document.getElementById('logged-user').innerText=`logged as ${res.username}`
        }
    })
}


const linkButtons = document.querySelectorAll('.link-button');

const linkClicked = (e) => {
    //const startTime = performance.now();
    var source = e.srcElement.innerHTML;
    listSearchItems.length = 0;
    listSearchItems = links.init(source)
    links.render()
    //const duration = performance.now() - startTime;    
    //console.log(`linkClicked took ${duration}ms`);
    //console.log(listSearchItems)
}
const searchEvent = (e) => {
    var regex = new RegExp(e.srcElement.value, "i");
    search.reset()
    if (e.srcElement.value.length >= 1) {
        search.init()
        var matchedArray = listSearchItems.filter(item => regex.test(item.name))
        search.render(matchedArray)
    }
    else {
        search.reset()
    }
}



const clickedResult = (e) => {
    var name = document.querySelectorAll('.item-name')[e.detail.index].innerText
    var type = document.querySelectorAll('.item-type')[e.detail.index].innerText
    var source = document.querySelectorAll('.searchresultlist')[e.detail.index].getAttribute('data-source')
    manage.init(source, type, name)
    manage.render()    
}

list.listen('MDCList:action', clickedResult)

const searchInput = document.getElementById('search');
searchInput.addEventListener('keyup', searchEvent);


document.querySelector('.home').addEventListener('click', () => {
    linkContent.style.display = "none";
});


linkButtons.forEach(linkButton => {
    linkButton.addEventListener('click', linkClicked);
});

document.querySelector('.home').addEventListener('click', (e) => {
    home.init()
})

document.querySelector('.login-button').addEventListener('click',()=>{    
    login.init()
    login.render()
})