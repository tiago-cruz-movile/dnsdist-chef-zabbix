#!/usr/bin/python -W ignore

"""
DNSDist - jsonstat
"""

import requests
from requests.auth import HTTPBasicAuth
from optparse import OptionParser
import socket
import json

parser = OptionParser(usage='%prog [-h] [--help]', version='%prog 0.1')
parser.add_option('-d', action='store_true', dest='debug', help='Debug')
(options, args) = parser.parse_args()

hostname=socket.gethostname()
url="http://localhost:8083/api/v1/servers/localhost"
key="<%= @key %>"

if options.debug: print "Checking '%s' with key '%s'" % ( url, key )

r = requests.get(url, auth=HTTPBasicAuth( 'admin', key ))
if r.status_code == 200:
  for i in r.json()['servers']:
    name = i.get('name')
    print hostname + " latency[" + name + "] " + str(i.get('latency'))
    print hostname + " outstanding[" + name + "] " + str(i.get('outstanding'))
    print hostname + " qps[" + name + "] " + str(i.get('qps'))
    print hostname + " queries[" + name + "] " + str(i.get('queries'))
    print hostname + " state[" + name + "] " + str(i.get('state'))

else:
  print "ERROR: HTTP request failed"
  print r.status_code

