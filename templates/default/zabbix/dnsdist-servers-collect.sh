#!/usr/bin/env bash
# collect dnsdist servers stats and send to zabbix

TMPFILE=`mktemp`
/movile/monitoring/dnsdist-get-servers-status.py > $TMPFILE
/usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -i $TMPFILE
[ -z $1 ] || cat $TMPFILE
rm -f $TMPFILE

