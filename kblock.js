var _iframe = document.getElementById('iframe');
var _origin = new URL(_iframe.src).origin;
var _host = window.location.host
console.log("host", _host)
var ws;
var _id = 0;

function connect() {
    ws = new WebSocket(`ws://${_host}/ws`);
    ws.onopen = function() {
        console.log('ws open');
    }
    
    ws.onmessage = function(e) {
        try {
            sendNotify('data', {data: e.data})
        } catch (error) {
            console.warn(error)
        }
    }
    
    ws.onclose = function() {
        console.log('ws close');
        setTimeout(connect, 1000)
    }
    
    ws.onerror = function(e) {
        console.log('ws error');
    }    
}

function sendResponse(id, result) {
    const resp = {id, result, jsonrpc: '2.0'}
    _iframe.contentWindow.postMessage(resp, _origin)
}

function sendError(id, error) {
    const resp = {id, error, jsonrpc: '2.0'}
    _iframe.contentWindow.postMessage(resp, _origin)
}

function sendRequest(method, params) {
    const req = {id: _id, method, params, jsonrpc: '2.0'}
    _iframe.contentWindow.postMessage(req, _origin)
    _id += 1
}

function sendNotify(method, params) {
    const req = {method, params, jsonrpc: '2.0'}
    _iframe.contentWindow.postMessage(req, _origin)
}


window.addEventListener('message', function(e) {
    if (e.origin !== _origin) {
      return;
    }
    const data = e.data;
    if (data.jsonrpc !== '2.0') {
      return;
    }
    const id = data.id;
    if (data.method === 'listdevice') {
        if (ws.readyState === WebSocket.OPEN) {
            sendResponse(id, [{name: _host, peripheralId: _host, type: 'web'}])
        } else {
            sendResponse(id, [])
        }
    } else if (data.method === 'connect'){
        sendResponse(id, {result: 'ok'})
    } else if (data.method === 'disconnect'){
        sendResponse(id, {result: 'ok'})
    } else if (data.method === 'get-disk'){
        sendResponse(id, "webfs")

    } else if (data.method === 'write'){
        ws.send(data.params.data)
    } else if (data.method === 'upload-file'){
        fetch(`http://${_host}/upload`, {
            method: 'POST',
            body: JSON.stringify(data.params)
        }).then((resp) => {
            sendResponse(id, {result: 'ok'})
        })
    } else {
        console.warn('unknown method', data.method)
        sendResponse(id, 'unknown method')
    }
});

connect();