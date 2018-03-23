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
url="http://localhost:8083/jsonstat?command=stats"
key="<%= @key %>"

if options.debug: print "Checking '%s' with key '%s'" % ( url, key )

r = requests.get(url, auth=HTTPBasicAuth( 'admin', key ))
if r.status_code == 200:
  for k,v in r.json().iteritems():
    print "%s %s %s" % ( hostname, k, v )
else:
  print "ERROR: HTTP request failed"
  print r.status_code

