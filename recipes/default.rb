#
# Cookbook:: dnsdist
# Recipe:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.

if not tagged?("dnsdist_#{node['datacenter']}")
  raise("Error: #{node['fqdn']} is not tagged to be part of a DNS HA cluster in datacenter: #{node['datacenter']}")
  return
end

include_recipe 'chef-vault'

# search
node.default[:dnsdist][:cluster_name] = "dnsdist_#{node['datacenter']}"
tagged_cluster_name = 'tags:' + "#{node[:dnsdist][:cluster_name]}"
cluster_nodes = search(:node, tagged_cluster_name, :filter_result => 
                              {'name' => [ 'hostname' ],
                               'ip'   => [ 'ipaddress' ]}) 
# dnsdist
package 'dnsdist'

execute 'check-dnsdist-config' do
  action :nothing
  command 'dnsdist --check-config'
  notifies :restart, 'service[dnsdist]', :delayed
end

dnsdist = chef_vault_item('dnsdist', 'dnsdist')

template '/etc/dnsdist/dnsdist.conf' do
  owner 'dnsdist'
  mode  '0640'
  variables(
    :cluster_nodes => cluster_nodes,
    :key => dnsdist['key']
  )
  notifies :run, 'execute[check-dnsdist-config]'
end

service 'dnsdist' do
  action [ :enable, :start ]
end
