# Server Management
```bash
openstack help server *for managing instances
openstack help server create *help for all commands
openstack server IMAGE create SERVER --name IMAGE_NAME
openstack server create ... --key-name NAME
openstack server create --image cirros --flavor 1 --network private myinstance
openstack server create --property db=10.100.100.6 *key value pair *can be used multiple times
openstack server create	--user-data install.sh *execute a script
openstack server create --user-data FILE *cloud-config file
openstack server create ... --config-drive=true *looks like a cdrom to the VM
openstack server show SERVER
openstack server stop SERVER
openstack server start SERVER
```
also deletes disk
```bash
openstack server delete SERVER 
openstack server add security group SERVER SECGROUP
openstack server remove security group SERVER SECGROUP
openstack flavor list
openstack server add floating ip SERVER_IP
openstack server remove floating ip SERVER_IP
openstack console url show SERVER
openstack console log show SERVER
```
query nova via api
```bash
curl http://192.168.1.61/compute/v2.1/servers -H "x-auth-token: $T" | python3 -m json.tool 
```

# Security Groups
```bash
openstack security group create NAME
openstack security group rule create --dst-port XX --protocol tcp NAME
```
yaml format may be easier to read 
```bash
openstack security group list --fit-width -f yaml --long 
```
long shows direction
```bash
openstack security group rule list NAME --long
```

# Floating IP
```bash
openstack floating ip list
openstack floating ip create EXT_NET
openstack floating ip delete IP_ADDR
```

# SSH Key Pairs
```bash
openstack keypair create NAME >key.pem
chmod 600 key.pem
openstack keypair create --public-key key.pub *add existing pub key
openstack keypair show --public-key NAME
openstack keypair list
```

# Networks
```bash
openstack network list
openstack network create NETWORK
openstack network set --name OLD NEW
```
## Subnets 
*DNS Is Configured on Subnets*
host route is like a static route
```bash
openstack subnet set SUBNET --dns-nameserver=[IP address] --host-route destination=[subnet CIDR],gateway=[IP] 
openstack subnet create NETWORK-subnet --network NETWORK --subnet range x.x.x.x 
```
## External networks
*for external network, for flat, openstack subnet must match physical iface subnet*
create network
```bash
openstack network create --external --provider-network-type flat --provider-physical-network [phy_nic] [net_name]
```
```bash
openstack subnet create --network [external network name]  --subnet-range 203.0.113.0/24 --gateway [physical router IP]  --allocation-pool start=[ipv4 least start],end=[ipv4 lease end] --dns-nameserver 8.8.8.8 [public-subnet-name]
```

# Routers
```bash
openstack router create ROUTER
openstack router add subnet ROUTER SUBNET
openstack router set [router name] --external-gateway [external network name]
openstack router create ROUTER
openstack router add subnet ROUTER SUBNET
openstack router add subnet ROUTER SUBNET2
openstack router add port PORT_NAME ROUTER
openstack port create PORT_NAME --network NETWORK
```

# Check for Endpoints
```bash
openstack endpoint list
openstack endpoint list --service [service ex. identity]
```

# Key Pair
```bash
openstack keypair create KEY_NAME > MY_KEY.pem
```

# Create / Manage Projects, Users, Roles; User Must Have Project to Log In
list all roles in openstack
```bash
openstack role list 
```
roles assigned to user
```bash
openstack role assignment list --user [user_name] --project [project_name] --names 
```
list users & roles in a project
```bash
openstack role assignment list --project [project_name] --names 
openstack project create --domain [dom name] --description "[description]" [project name]
openstack role add --project [project name] --user [username] [role]
```

# Glance Management
```bash
openstack image create --disk-format qcow2 --container-format bare --public --file ./centos63.qcow2 centos63-image
openstack image list
```
check if image is accessible and available; json optional
```bash
openstack image show <image_id> -f json 
```
download
```bash
openstack image save --file test_image.img <image_id>
```

# Neutron & Network Management
```bash
openstack network agent list
openstack network service provider list
```

# OpenVSwitch Management
## OpenStack Requirements
- br-provider
  - port-provider -> Phy port
  - port-internal -> local ip
- br-int
  - port-int -> port-tun
- br-tun
  - port-tun -> port-int

## Network Manager
```bash
nmcli con add type ethernet ifname [link name] con-name [onboot-ovs] ipv4.method disabled ipv6.method ignore connection.autoconnect yes # required profile for bridge
```
## Native OVS
### Show Commands
```bash
ovs-vsctl show # open vswitch list of bridges
ovs-vsctl list-br # br-tun should be present for vxlan or other tunneling
ovs-vsctl list Open_vSwitch # list config db for open vSwitch
ovs-vsctl list interface
ovs-ofctl dump-flows br-tun # checks openflow rules
ovs-appctl fdb/show br-enp2s0 # show known mac addresses
```
### Create Commands
```bash
ovs-vsctl add-br [new bridge name]
ovs-vsctl add-port [bridge name] [phy dev] 
ovs-vsctl add-br br-tun
ovs-vsctl add-port br-tun vxlan0 -- set interface vxlan0 type=vxlan options:local_ip=172.22.2.21 options:remote_ip=flow options:key=flow
```

# Cinder Management
```bash
openstack volume pool list --long
openstack volume backend pool list
openstack volume service list
```

# Nova Management
```bash
openstack compute service list # parts of nova; requires admin
nova compute service list --service [nova-compute or other]
openstack hypervisor list # should be listed with a nonzero number of free VCPUs, RAM, and disk space
openstack hypervisor show [identifier]
openstack usage list
openstack quota show
```
