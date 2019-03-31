#!/usr/bin/python
from flask import Flask, request, Response
import json

app = Flask(__name__)

myResponses = {
    "POST"  : {},
    "GET"   : {},
    "PUT"   : {},
}
#method:url:dict

debug = False


with open('responses.json') as json_file:  
    data = json.load(json_file)

for d in data:
    path = d['request']['url'][25:].split('?', 1)[0]
    myResponses[d['request']['method']][path] = d


@app.route('/')
def hello():
    return "Fireline Emulator for Fractured Space v0.1.0"


@app.route('/<path:path>', methods = myResponses.keys())
def hello_name(path):
    canned = lookup(request.method, path)
    print(request.query_string)
    if canned is None:
        payload = "Method: {}\n".format(request.method)
        payload += "Path: {}\n".format(path)
        payload += "Data: {}\n".format(len(myResponses))
        payload += "\n".join(myResponses['GET'].keys())
        
        resp = Response(response=json.dumps({"ERROR":payload}),
                        status=200,
                        mimetype="application/json")
        if debug : print(">>>MISS") 
    else:
        resp = Response(response=canned['response']['content'],
                        status=canned['response']['status_code'],
                        mimetype="application/json")
        if debug : print("hit") 


    return resp

def lookup(method, path):
    if method in myResponses.keys():
        if path in myResponses[method].keys():
            return myResponses[method][path]
    return None

if __name__ == '__main__': 
    debug = True
    app.run(threaded=True, port=8080, debug=True)
