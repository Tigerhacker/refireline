from flask import Flask, request, Response
import json
import re
from time import sleep
import os

app = Flask(__name__)

myResponses = {
    "POST"  : {},
    "GET"   : {},
    "PUT"   : {},
    "PATCH"   : {},
}
#method:url:dict

debug = False


# with open('responses-cleaned.json') as json_file:  
#     myResponses = json.load(json_file)
for filename in os.listdir('responses'):
    if filename.endswith(".json"): 
        path = os.path.join('responses', filename)
        with open(path) as json_file:  
            response = json.load(json_file)
            method = response['request']['method']
            path = response['path']
            myResponses[method][path] = response
        continue
    else:
        continue


# def presence()


@app.route('/')
def hello():
    return "Fireline Emulator for Fractured Space v0.1.0"


@app.route('/presence/connect')
def poll():
    print("!!!CONNECT: {}".format(request.headers))
    def generate():
        yield '["welcome",{"success":true,"data":{"connection_id":"180182b9-ee86-4442-8ba5-2df0aad31e20","connected_at":"Sun, 31 Mar 2019 13:06:12 GMT"}}]\n'
        for i in xrange(300):
            print("!!!presence: {}".format(i))
            sleep(1)
            yield "\n"
    return Response(generate(), mimetype='application/x-json-stream')

import re, json
from endpoint_o_instances__metadata import handler as o_inst_meta
from endpoint_o_sessions_create import handler as o_sess_crea
from endpoint_o_instances__associate_with_session import handler as o_inst_asso
from endpoint_o_sessions__metadata import handler as o_sess_meta

def hello_world(request, match):
    return (200, "Hello {}!".format(match.group(1)), {})

DYNAMIC_HANDLERS = {
    r'^o/_instances/([^/]+)/metadata': o_inst_meta,
    r'^o/_sessions/create': o_sess_crea,
    r'o/_instances/([^/]+)/associate_with_session': o_inst_asso,
    r'o/_sessions/([^/]+)/metadata': o_sess_meta,
    r'^hello/(.*)/': hello_world,
}

def get_dynamic(path, request):
    response = None
    for regex, handler in DYNAMIC_HANDLERS.items():
        match = re.match(regex, path)
        if match:
            response = handler(request, match)
            break
    return response

@app.route('/<path:path>', methods = myResponses.keys())
def main_handler(path):
    payload = "Method: {}\n".format(request.method)
    payload += "Path: {}\n".format(path)
    payload += "Data: {}\n".format(len(myResponses))

    dynamic = get_dynamic(path, request)

    if dynamic is not None:
        (status, payload, headers) = dynamic
        resp = Response(response=json.dumps(payload),
                        status=status,
                        headers=headers,
                        mimetype="application/json")
        return resp

    canned = lookup(request.method, path)
    print(request.query_string)
    if canned is None:
        payload += "\n".join(myResponses['GET'].keys())
        resp = Response(response=json.dumps({"ERROR":payload}),
                        status=200,
                        mimetype="application/json")
        if debug : print(">>>MISS")
        if debug : print(path)
    else:
        resp = Response(response=json.dumps(canned['response']['content']),
                        status=canned['response']['status_code'],
                        mimetype="application/json")
        if debug : print("hit")


    return resp

def strip_identity(path):
    return re.sub(r'/_identities/[^/]+/', '/_identities/00000000-0000-0000-0000-000000000000/', path)

def lookup(method, path):
    # path = strip_identity(path)
    if method in myResponses.keys():
        if path in myResponses[method].keys():
            return myResponses[method][path]
    return None

if __name__ == '__main__':
    debug = True
    
    app.run(threaded=True, port=8080,debug=True)
