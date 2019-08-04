from flask import Flask, request, Response
import json
import re
from time import sleep
import os

app = Flask(__name__)
application = app

myResponses = {
    "POST"  : {},
    "GET"   : {},
    "PUT"   : {},
    "PATCH"   : {},
    "DELETE"   : {},
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
    return "Fireline Emulator for Fractured Space v0.2.0"


@app.route('/presence/connect')
def poll():
    print("!!!CONNECT: {}".format(request.headers))
    def generate():
        yield '["welcome",{"success":true,"data":{"connection_id":"180182b9-ee86-4442-8ba5-2df0aad31e20","connected_at":"Sun, 31 Mar 2019 13:06:12 GMT"}}]\n'
        for i in xrange(300):
            # print("!!!presence: {}".format(i))
            sleep(1)
            yield "\n"
    return Response(generate(), mimetype='application/x-json-stream')

import re, json
from endpoint_auth_oauth2_token import handler as auth_oaut_tokn
from endpoint_o_instances_register import handler as o_inst_regi
from endpoint_o_instances__metadata import handler as o_inst_meta
from endpoint_o_sessions_create import handler as o_sess_crea
from endpoint_o_instances__associate_with_session import handler as o_inst_asso
from endpoint_o_sessions__metadata import handler as o_sess_meta
from endpoint_o_sessions__touch import handler as o_sess_toch
from endpoint_o_instances_list import handler as o_inst_list
from endpoint_o_sessions__reservations import handler as o_sess_rsvp

def hello_world(request, match):
    return (200, "Hello {}!".format(match.group(1)), {})

DYNAMIC_HANDLERS = {
    r'^auth/oauth2/token': auth_oaut_tokn,
    r'^o/_instances/register': o_inst_regi,
    r'^o/_instances/([^/]+)/metadata': o_inst_meta,
    r'^o/_sessions/create': o_sess_crea,
    r'o/_instances/([^/]+)/associate_with_session': o_inst_asso,
    r'^o/_sessions/([^/]+)/metadata': o_sess_meta,
    r'^o/_sessions/([^/]+)/touch': o_sess_toch,
    r'^o/_instances/list': o_inst_list,
    r'^o/_sessions/([^/]+)/reservations(?:/([^/]+))?': o_sess_rsvp,
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
        headers['Cache-Control'] = 'no-cache'
        resp = Response(response=json.dumps(payload),
                        status=status,
                        headers=headers,
                        mimetype="application/json")
        return resp

    detected_userid = None
    if 'Authorization' in request.headers:
        detected_userid = request.headers['Authorization'][7:]
        print("Hello user: {}".format(detected_userid))
    canned = lookup(request.method, path, detected_userid)
    print(request.query_string)
    if canned is None:
        payload += "\n".join(myResponses['GET'].keys())
        resp = Response(response=json.dumps({"ERROR":payload}),
                        status=404,
                        mimetype="application/json")
        if debug : print(">>>MISS")
        if debug : print(path)
    else:
        print("{}".format(request.headers))
        if detected_userid is not None:
            canned_mod = sub_outgoing(canned, detected_userid)
        resp = Response(response=json.dumps(canned_mod['response']['content']),
                        status=canned_mod['response']['status_code'],
                        mimetype="application/json")
        if debug : print("hit")


    return resp

def strip_incoming_identity(path, detected_userid):
    #not really, but we are setting it to what we recorded
    if detected_userid is None:
        return re.sub(r'/_identities/[^/]+/', '/_identities/197a97fc-4179-43f4-b009-9432ac0c8e53/', path)
    else:
        if re.match('^o/player_status/', path):
            return re.sub(r'o/player_status/.*', 'o/player_status/38662703-6375-3ae3-8558-1a2238c0f088', path)
        elif re.match('^o/player_data/', path):
            return re.sub(r'o/player_data/.*', 'o/player_data/11f07816-c552-331d-a81c-4b43f126d7bf', path)
        elif re.match('^o/player_info/', path):
            return re.sub(r'o/player_info/.*', 'o/player_info/d649cb45-cc6e-3914-ba71-d84cfa9db5e0', path)
        elif re.match('^o/player_wallet/', path):
            return re.sub(r'o/player_wallet/.*', 'o/player_wallet/b474182f-f5b4-3518-b1bc-d06fe5e4ca23', path)
        elif re.match('^o/crew_meta/', path):
            return re.sub(r'o/crew_meta/.*', 'o/crew_meta/9dbfee14-f265-35a5-b572-0c018a39faca', path)
        elif re.match('^o/player_stats/', path):
            return re.sub(r'o/player_stats/.*', 'o/player_stats/bc7f731e-6af2-3f60-a2e0-5d938d5e3340', path)
        elif re.match('^o/player_medals/', path):
            return re.sub(r'o/player_medals/.*', 'o/player_medals/857ae962-0d37-35a6-95ee-9c549d11365f', path)
        else:
            return path.replace(detected_userid, '197a97fc-4179-43f4-b009-9432ac0c8e53')

def sub_outgoing0(payload, new_string, old_string="197a97fc-4179-43f4-b009-9432ac0c8e53"):
    '''Scan outgoing data for my user-uid and replace it with the auto-generated one
    '''
    new = {}
    for k, v in payload.iteritems():
        if isinstance(v, dict):
            new['k'] = sub_outgoing(v, new_string, old_string)
        elif v == old_string:
            print("{}:{}".format(k, v))
            new[k] = new_string
        else:
            new['k'] = v

    return new

def sub_outgoing(payload, new_string, old_string="197a97fc-4179-43f4-b009-9432ac0c8e53"):
    return  json.loads(json.dumps(payload).replace(old_string, new_string))

def lookup(method, path, detected_userid=None):
    path = strip_incoming_identity(path, detected_userid)
    if method in myResponses.keys():
        if path in myResponses[method].keys():
            return myResponses[method][path]
    return None

if __name__ == '__main__':
    debug = True
    
    app.run(threaded=True, port=8080,debug=True)
