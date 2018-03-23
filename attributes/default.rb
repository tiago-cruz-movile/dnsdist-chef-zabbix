# port used in dnsdist to 
# accept DNS queries on UDP/TCP port
default[:dnsha][:lb_port] = "53" 

# bind backend port (running in localhost)
default[:dnsha][:backend_port]  = "553" 
