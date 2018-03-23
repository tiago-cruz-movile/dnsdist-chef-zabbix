#
# Cookbook:: dnsha
# Recipe:: zabbix
#
# Copyright:: 2018, The Authors, All Rights Reserved.


package "python-requests"

cookbook_file "/etc/zabbix/zabbix_agentd.d/dnsdist.conf" do
  owner "root"
  mode  "0644"
end

dnsdist = chef_vault_item('dnsha', 'dnsdist')
[ "dnsdist-discovery-servers.py", "dnsdist-get-servers-status.py", "dnsdist-stats.py", 
  "dnsdist-status-collect.sh", "dnsdist-servers-collect.sh"].each do |zbx|
  template "/movile/monitoring/#{zbx}" do
    source "zabbix/#{zbx}"
    group "zabbix"
    mode "0750"
    variables(
      :key => dnsdist['key']
    )
  end
end

