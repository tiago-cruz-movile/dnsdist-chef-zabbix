#!/usr/bin/python -W ignore

"""
DNSDist - jsonstat
"""

import requests
from requests.auth import HTTPBasicAuth
from optparse import OptionParser
import json

parser = OptionParser(usage='%prog [-h] [--help]', version='%prog 0.1')
parser.add_option('-d', action='store_true', dest='debug', help='Debug')
(options, args) = parser.parse_args()

url="http://localhost:8083/api/v1/servers/localhost"
key="<%= @key %>"

if options.debug: print "Checking '%s' with key '%s'" % ( url, key )

server_list = []
r = requests.get(url, auth=HTTPBasicAuth( 'admin', key ))
if r.status_code == 200:
  for i in r.json()['servers']:
    server_name = i.get('name').lower()
    servers = { "{#SERVER_NAME}": server_name }
    server_list.append(servers)
  print json.dumps({"data":server_list})

else:
  print "ERROR: HTTP request failed"
  print r.status_code

