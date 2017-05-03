# Proxy for CloudShell Live
# HTTP server on port 5000
# Access to https://demo.quali.com:3443 for clients that reject the certificate and can't ignore certificates
# Adds functionality to some calls (see function comments)

from flask import Flask, request
import requests
import json
import time
import re

app = Flask(__name__)


@app.route('/api/login', methods=['PUT', 'GET'])
def a():
    # log in
    # matches the CloudShell API
    print request.get_data()
    s = requests.put('https://demo.quali.com:3443/api/login', verify=False, headers={'Content-Type': 'application/json'}, data=request.get_data()).text
    return '[' + s + ']'


@app.route('/api/v2/blueprints/<bpname>/start', methods=['POST'])
def b(bpname):
    # starts sandbox
    # same input as the 'start' API
    # after starting, polls status until Setup has finished
    # returns the output of the 'start' call
    # be sure to set a long timeout in the client (e.g. 10 min)
    print request.url
    print request.get_data()
    r = requests.post('https://demo.quali.com:3443/api/v2/blueprints/%s/start' % bpname, verify=False, headers=request.headers, data=request.get_data())
    if r.status_code >= 400:
        raise Exception('Error %d: %s' % (r.status_code, r.text))
    s = r.text
    print s
    sbid = json.loads(s)['id']
    auth = request.headers['Authorization']
    headers = {'Authorization': auth}
    print request.get_data()
    state = ''
    j = ''
    for i in range(100):
        print 'getting status'
        url = 'https://demo.quali.com:3443/api/v2/sandboxes/%s' % sbid
        print 'url=%s headers=%s' % (url, headers)
        j = requests.get(url, verify=False, headers=headers).text
        if j:
            j = json.loads(j)
            state = j['state']
            print 'status %s' % state
            if state in ['Error', 'Ready']:
                break
        else:
            print 'null status'
        time.sleep(5)
    if state not in ['Error', 'Ready']:
        raise Exception('Timeout waiting for sandbox %s to become available' % sbid)
    print 'Returning: %s' % s
    return s


@app.route('/api/v2/sandboxes/<sbname>/stop', methods=['POST'])
def c(sbname):
    # DON'T USE, official v2 stop API erroneously rejects its official input
    # stops the sandbox
    # same as official 'stop' API
    # returns raw 'stop' output
    print request.get_data()
    s = requests.post('https://demo.quali.com:3443/api/v2/sandboxes/%s/stop' % sbname, verify=False, headers=request.headers, data=request.get_data()).text
    print s
    return s


@app.route('/api/v1/sandboxes/<sbname>/stop', methods=['POST'])
def c1(sbname):
    # note: v1 version of the API
    # same as official 'stop' API
    # returns raw 'stop' output
    print request.get_data()
    s = requests.post('https://demo.quali.com:3443/api/v2/sandboxes/%s/stop' % sbname, verify=False, headers=request.headers, data=request.get_data()).text
    print s
    return s


@app.route('/delay30')
def d60():
    # use to sleep 30 seconds in a client that can't do anything but REST calls
    time.sleep(30)
    return '{"statusCode":200,"message":"finished waiting"}'


@app.route('/tests')
def d():
    # return a static message immediately
    return 'tests run'


@app.route('/api/v2/sandboxes/<sbid>/components/<comppatt>/commands/<commandname>/start', methods=['POST'])
def e(sbid, comppatt, commandname):
    # starts a command
    # instead of taking a component id like the official API, takes a regex and searches the sandbox for the first matching component
    # same input body as official API
    # after starting the command, polls until it completes
    # returns {"statusCode": <200 or 400>, "message": "<command result>"}
    # will end only with a timeout if the test ends with an unknown status (other than Completed, Error, Failed, Stopped)
    compid = ''
    auth = request.headers['Authorization']
    headers = {'Authorization': auth}
    print request.get_data()
    #print 'sleeping 30 seconds before command'
    #time.sleep(30)
    state = ''
    j = ''
    url = 'https://demo.quali.com:3443/api/v2/sandboxes/%s' % sbid
    print 'url=%s headers=%s' % (url, headers)
    j = requests.get(url, verify=False, headers=headers).text
    print 'sandbox status: %s' % j
    j = json.loads(j)
    for c in j['components']:
        if re.search(comppatt, c['name']):
            compid = c['id']
            break
    if not compid:
        raise Exception('No component found matching pattern %s' % comppatt)
    s = requests.post('https://demo.quali.com:3443/api/v2/sandboxes/%s/components/%s/commands/%s/start' % (sbid, compid, commandname), verify=False, headers=request.headers, data=request.get_data()).text
    o = json.loads(s)
    if '_links' in o:
        statusurl = 'https://demo.quali.com:3443/api/v2%s' % o['_links']['self']['href']
        for _ in range(50):
            s = requests.get(statusurl, verify=False, headers=headers).text
            o = json.loads(s)
            print 'Run status: %s' % o['status']
            if o['status'] in ['Completed', 'Error', 'Failed', 'Stopped']:
                ov = (o['output'] or 'Test completed successfully').strip()
                rv = '{"statusCode":%d,"message":"%s"}' % (201 if o['status'] == 'Completed' else 400, ov)
                print 'returning %s' % rv
                return rv
            time.sleep(5)
    rv = '{"statusCode":400, "message":"Test did not reach Completed, Error, Failed, or Stopped within 250 seconds"}'
    print 'returning %s' % rv
    return rv

app.run(host='0.0.0.0')
# listen on port 5000
