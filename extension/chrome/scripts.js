"use strict";

const DOMAIN = "http://127.0.0.1:8000";

let sections = ["login", "submit", "fail", "ok"];
let form = null;
let url = "";

//Time to wait before closing the window automatically
const WAIT_TIME = 3000;

// Display the given section, then hide the rest
let switchSection = function(sect) {
    for(let s of sections) {
        document.getElementById(s).style.display = "none";
    }
    
    document.getElementById(sect).style.display = "block";
};

chrome.runtime.onMessage.addListener(([type, data], sender) => {
    switch(type) {
        case "submitDone":
            // Submiting a bookmark is complete, data is true if we were successful, false if an error happened
            if(data) {
                switchSection("ok");
                setTimeout(() => window.close(), WAIT_TIME);
            }else{
                switchSection("fail");
                setTimeout(() => switchSection("submit"), WAIT_TIME);
            }
    }
});

// Submit the add bookmark form
let submit = function(e) {
    e.preventDefault();
    
    let obj = {};
    obj.url = url;
    obj.title = form.title.value;
    obj.valid_url = true;
    if(form.tags.value) {
        obj.tags = form.tags.value.split(",");
    }else{
        obj.tags = [];
    }
    
    chrome.runtime.sendMessage(["submit", obj]);
}

// The first thing we do is look for a session cookie, and see if we are logged in
chrome.cookies.get({"url":DOMAIN, "name":"sessionid"}, (c) => {
    if(!c) {
        switchSection("login");
    }else{
        chrome.tabs.query({active:true, currentWindow:true}, (t) => {
            t = t[0];
            form = document.getElementById("submitForm");
            form.onsubmit = submit;
            
            url = t.url;
            form.title.value = t.title;
            
            form.title.focus();
            
            switchSection("submit");
        });
    }
});

// And set the "login" link to point to the site
document.getElementById("login-link").href = DOMAIN;
