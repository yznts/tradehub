

function _PipePopup() {
    
    this.listeners = {};

    this._pipe_listener = function (request) {
        if (!this.listeners[request.action]) {
            return;
        }
        this.listeners[request.action].forEach(function(listener) {
            listener(request.data);
        })
    };

    this.addActionListener = function (action, callback) {
        if (!this.listeners.action)
            this.listeners[action] = [];
        this.listeners[action].push(callback);
    };

    this.sendMessage = function (action, data, callback) {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {action: action, data: data}, function(response){callback()});
        });
    }
}

function _PipeContent() {

    this.listeners = {};

    this._pipe_listener = function (request) {
        if (!this.listeners[request.action]) {
            return;
        }
        this.listeners[request.action].forEach(function(listener) {
            listener(request.data);
        })
    };

    this.addActionListener = function (action, callback) {
        if (!this.listeners.action)
            this.listeners[action] = [];
        this.listeners[action].push(callback);
    };

    this.sendMessage = function (action, data, callback) {
        chrome.runtime.sendMessage({action: action, data: data}, function(response){callback()});
    }
}
    
const PipePopup = new _PipePopup();
const PipeContent = new _PipeContent();

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        PipePopup._pipe_listener(request);
    }
);
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        PipeContent._pipe_listener(request);
    }
);