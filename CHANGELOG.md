## CHANGELOG

 - 1.0.0 - cluster keepalive + nginx + named workinig
 - 1.0.1 - cluster members addedd/removed with chef search based on tag + datacenter
 - 1.0.2 - auth_pass in knife vault
 - 1.0.3 - Adde monitoring scripts for zabbix from: https://github.com/lesovsky/zabbix-extensions/tree/master/files/keepalived
 - 1.0.4 - Ajusts in monitoring. Floating IP is monitored and any changing in state (migration from one machine to another) will generate a problem that must be closed by operador
 - 1.0.5 - Removing nginx since UDP-LB not working propertly
 - 1.0.6 - Added support to dnsdist
