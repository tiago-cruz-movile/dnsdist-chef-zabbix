# Cookbook dnsdist
  This cookbook implements a dnsdist to use with named HA environment.

## Environment

- Centos 7
- Zabbix 3.2
- Chef 12

## Chef

  - Description of 'recipe[dnsdist::default]':
  - We use `node['datacenter']` in `role[base]` to discover the datacenter name of each node
  - We use 02 dnsdist servers in every datacenter, listen in port 53 tcp/udp
  - Each dnsdist server will balance the load to a bind/named server running in localhost, listen in 553 tcp/udp
  - Members of the cluster ares searched by tag: `dnsdist_node['datacenter'].`
  - You must tag each cluster node with a tag in this format. Ex: `knife tag create <host> "dnsdist_equinix"`
  - Only one cluster exists in each DC (with same id)
  - Vault must be updated for every remove/addiction of nodes
	- Ex: `knife vault update dnsha dnsdist -S 'tags:dnsdist_equinix'`

## Zabbix

  - Description of 'recipe[dnsdist::zabbix]':
  - Import the template `templates/default/zabbix/Template_DNSDist_Zabbix_v3.2.xml` to your zabbix server
  - The zabbix-agent configuration will looks like this:

```
[root@dnsdist1 ~]# cat /etc/zabbix/zabbix_agentd.d/dnsdist.conf 
# DNSDist monitoring
UserParameter=dnsdist-status-collect,(/movile/monitoring/dnsdist-status-collect.sh > /dev/null; echo $?)
UserParameter=dnsdist-servers-collect,(/movile/monitoring/dnsdist-servers-collect.sh > /dev/null; echo $?)
UserParameter=dnsdist-discovery-servers,/movile/monitoring/dnsdist-discovery-servers.py
```

 - Every collect shell script has a 'debug':


```
[root@dnsdist1 ~]# /movile/monitoring/dnsdist-servers-collect.sh debug
info from server: "processed: 10; failed: 0; total: 10; seconds spent: 0.000355"
sent: 10; skipped: 0; total: 10
dnsdist1.datac.com latency[dnsdist1] 135
dnsdist1.datac.com outstanding[dnsdist1] 0
dnsdist1.datac.com qps[dnsdist1] 0
dnsdist1.datac.com queries[dnsdist1] 250050
dnsdist1.datac.com state[dnsdist1] up
dnsdist1.datac.com latency[dnsdist2] 135
dnsdist1.datac.com outstanding[dnsdist2] 0
dnsdist1.datac.com qps[dnsdist2] 0
dnsdist1.datac.com queries[dnsdist2] 249733
dnsdist1.datac.com state[dnsdist2] up
```
 - The `dnsdist-discovery-servers.py` will be used to a low level discovery in zabbix:

```
[root@dnsdist1 ~]# /movile/monitoring/dnsdist-discovery-servers.py | jq .
{
  "data": [
    {
      "{#SERVER_NAME}": "dnsdist1"
    },
    {
      "{#SERVER_NAME}": "dnsdist2"
    }
  ]
}
```

- This #SERVER_NAME will be used to collect specific metrics about the server:

```
[root@dnsdist1 ~]# /movile/monitoring/dnsdist-servers-collect.sh debug
info from server: "processed: 10; failed: 0; total: 10; seconds spent: 0.000393"
sent: 10; skipped: 0; total: 10
dnsdist1.datac.com latency[dnsdist1] 130
dnsdist1.datac.com outstanding[dnsdist1] 0
dnsdist1.datac.com qps[dnsdist1] 0
dnsdist1.datac.com queries[dnsdist1] 250859
dnsdist1.datac.com state[dnsdist1] up
dnsdist1.datac.com latency[dnsdist2] 142
dnsdist1.datac.com outstanding[dnsdist2] 0
dnsdist1.datac.com qps[dnsdist2] 0
dnsdist1.datac.com queries[dnsdist2] 250536
dnsdist1.datac.com state[dnsdist2] up
```



## dnsdist

dnsdist is a highly DNS-, DoS- and abuse-aware loadbalancer. Its goal in life is to route traffic to the best server, delivering top performance to legitimate users while shunting or blocking abusive traffic.

more info: https://dnsdist.org/index.html

# cli

```
[tiago.cruz@dnsdist1 ~]$ dnsdist -c
> showServers()
#   Name                 Address                       State     Qps    Qlim Ord Wt    Queries   Drops Drate   Lat Outstanding Pools
0   dnsdist1             10.110.0.21:53                   up   126.8       0   1  1       1140       0   0.0   0.2           0 
1   dnsdist2             10.110.0.22:5 3                  up   126.9       0   1  1       1140       0   0.0   0.5           0 
All                                                            252.0                      2280       0                         
```

# built-in webserver 

- http://dnsdist1:8083/
- http://dnsdist2:8083/

Pass: `knife vault show dnsha dnsdist`

# json stats

```
[tiago.cruz@dnsdist1 ~]$ curl -s -XGET -u username:secret "localhost:8083/jsonstat?command=stats" | jq .
{
  "acl-drops": 0,
  "cache-hits": 0,
  "cache-misses": 0,
  "cpu-sys-msec": 641,
  "cpu-user-msec": 563,
  "downstream-send-errors": 0,
  "downstream-timeouts": 0,
  "dyn-block-nmg-size": 0,
  "dyn-blocked": 0,
  "empty-queries": 0,
  "fd-usage": 15,
  "latency-avg100": 385.2436005738687,
  "latency-avg1000": 370.1484730570304,
  "latency-avg10000": 131.7595022700412,
  "latency-avg1000000": 1.6214529289889317,
```


