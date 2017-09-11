"use strict";

const DOMAIN = "http://127.0.0.1:8000"
const SUBMIT_URL = DOMAIN + "/bookmarks/create";
const REFER_VALUE = DOMAIN + "/.chrome_extension";

let intercept = false;

// Call the callback with the csrf token (read from a cookie)
let getCsrf = function(callback) {
    chrome.cookies.get({"url":DOMAIN, "name":"csrftoken"}, (c) => {
        callback(c.value);
    });
};

// If intercept is true, intercept the request to the submit page and add the referer header (Django requires it to be
//  set)
chrome.webRequest.onBeforeSendHeaders.addListener((r) => {
    if(!intercept) return;
    r.requestHeaders.push({"name":"Referer", "value":REFER_VALUE});
    return {requestHeaders: r.requestHeaders};
}, {"urls":[SUBMIT_URL]}, ["blocking", "requestHeaders"]);

chrome.runtime.onMessage.addListener(([type, data], sender) => {
    switch(type) {
        case "submit":
            // A bookmark is to be submitted
            let toSub = JSON.stringify(data);
            intercept = true;
            
            getCsrf((token) => {
                fetch(SUBMIT_URL, {
                    "method":"POST", headers: {  
                        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "X-CSRFToken": token
                    },
                    body:"obj=" + toSub,
                    credentials:"include"
                }).then(function(res) {
                    intercept = false;
                    chrome.runtime.sendMessage(["submitDone", res.ok]);
                });
            });
    }
});
