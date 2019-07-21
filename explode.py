from flask import Flask, request, Response
import json
import re
from time import sleep

app = Flask(__name__)

myResponses = {
    "POST"  : {},
    "GET"   : {},
    "PUT"   : {},
}
#method:url:dict

debug = False


with open('responses-cleaned.json') as json_file:  
    myResponses = json.load(json_file)

for method, requests in myResponses.iteritems():
    for url, request in requests.iteritems():
        filename = url.replace('/', '___')
        filename = "responses/{}___{}.json".format(method, filename)
        with open(filename, 'w') as outfile:
            request['path'] = url
            json.dump(request, outfile, sort_keys=True, indent=4, separators=(',', ': '))