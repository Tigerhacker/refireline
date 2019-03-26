#!python

from mitmproxy import io
from mitmproxy.exceptions import FlowReadException
import pprint
import sys

inFile = "dump.out"

payload = []
allData = []

with open(inFile, "rb") as logfile:
    freader = io.FlowReader(logfile)
    pp = pprint.PrettyPrinter(indent=4)
    try:
        for f in freader.stream():
            data = {}
            data['request']={}
            data['request']['headers'] = [(x, f.request.headers.get(x)) for x in f.request.headers.keys()]
            data['request']['content'] = f.request.content.decode('ascii')
            data['request']['method'] = f.request.method
            data['request']['url'] = f.request.url
            #
            data['response']={}
            data['response']['status_code'] = f.response.status_code
            data['response']['headers'] = [(x, f.response.headers.get(x)) for x in f.response.headers.keys()]
            data['response']['content'] = f.response.content.decode('ascii')
            
            allData.append(f)
            payload.append(data)
    except FlowReadException as e:
        print("Flow file corrupted: {}".format(e))
        
import json

with open(inFile+'.json', 'w') as outfile:  
    json.dump(payload, outfile, sort_keys=True, indent=4, separators=(',', ': '))