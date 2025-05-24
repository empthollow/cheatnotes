### SERVER MANAGEMENT ###
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
openstack server delete SERVER *deletes disk
openstack server add security group SERVER SECGROUP
openstack server remove security group SERVER SECGROUP
openstack flavor list
openstack server add floating ip SERVER_IP
openstack server remove floating ip SERVER_IP
openstack console url show SERVER
openstack console log show SERVER
curl http://192.168.1.61/compute/v2.1/servers -H "x-auth-token: $T" | python3 -m json.tool # query nova via api
```

### SECURITY GROUPS ###
```bash
openstack security group create NAME
openstack security group rule create --dst-port XX --protocol tcp NAME
openstack security group list --fit-width -f yaml --long # foramt yaml may be easier to read *long shows direction
openstack security group rule list NAME --long
```

### FLOATING IP ###
```bash
openstack floating ip list
openstack floating ip create EXT_NET
openstack floating ip delete IP_ADDR
```

### SSH KEY PAIRS ###
```bash
openstack keypair create NAME >key.pem
chmod 600 key.pem
openstack keypair create --public-key key.pub *add existing pub key
openstack keypair show --public-key NAME
openstack keypair list
```

### NETWORKS ###
```bash
openstack network list
openstack network create NETWORK
openstack network create --external --provider-physical-network [provider <defined in ml2_conf.ini> ]  --provider-network-type flat [new nework name]  # create external network
openstack network set --name OLD NEW
```

### SUBNETS ; DNS IS CONFIGURED ON SUBNETS ###
```bash
openstack subnet set SUBNET --dns-nameserver=[IP address] --host-route destination=[subnet CIDR],gateway=[IP] # --host-route is like a static route
openstack subnet create NETWORK-subnet --network NETWORK --subnet range x.x.x.x 
openstack subnet create --network [external network name]  --subnet-range 203.0.113.0/24 --gateway [physical router IP]  --allocation-pool start=[ipv4 least start],end=[ipv4 lease end] --dns-nameserver 8.8.8.8 public-subnet # for external network, for flat, openstack subnet must match physical iface subnet
```

### ROUTERS ###
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

### CHECK FOR ENDPOINTS ###
```bash
openstack endpoint list
openstack endpoint list --service [service ex. identity]
```

### KEY PAIR ###
```bash
openstack keypair create KEY_NAME > MY_KEY.pem
```

### CREATE / MANAGE PROJECTS, USERS, ROLES ; USER MUST HAVE PROJECT TO LOG IN ###
```bash
openstack role list # list all roles in openstack
openstack role assignment list --user [user_name] --project [project_name] --names # roles assigned to user
openstack role assignment list --project [project_name] --names # list users & roles in a project
openstack project create --domain [dom name] --description "[description]" [project name]
openstack role add --project [project name] --user [username] [role]
```

### GLANCE MANAGEMENT ###
```bash
openstack image create --disk-format qcow2 --container-format bare --public --file ./centos63.qcow2 centos63-image
openstack image list
openstack image show <image_id> -f json # check if image is accessible and available; json optional
openstack image save --file test_image.img <image_id> # download
```

### NETWORK MANAGEMENT ###
```bash
openstack network agent list
openstack network service provider list
```

### OPENVSWITCH MANAGEMENT ###
```bash
nmcli con add type ethernet ifname [link name] con-name [onboot-ovs] ipv4.method disabled ipv6.method ignore connection.autoconnect yes # required profile for bridge
ovs-vsctl show # open vswitch list of bridges
ovs-vsctl add-br [new bridge name]
ovs-vsctl add-port [bridge name] [phy dev] # ip and routing needs to be configured manually
ovs-vsctl list-br # br-tun should be present for vxlan or other tunneling
ovs-vsctl list Open_vSwitch # list config db for open vSwitch
ovs-vsctl list interface
ovs-vsctl add-br br-tun
ovs-vsctl add-port br-tun vxlan0 -- set interface vxlan0 type=vxlan options:local_ip=172.22.2.21 options:remote_ip=flow options:key=flow
ovs-ofctl dump-flows br-tun # checks openflow rules
ovs-appctl fdb/show br-enp2s0 # show known mac addresses
```

### CINDER MANAGEMENT ###
```bash
openstack volume pool list --long
openstack volume backend pool list
openstack volume service list
```

### NOVA MANAGEMENT ###
```bash
openstack compute service list # parts of nova; requires admin
nova compute service list --service [nova-compute or other]
openstack hypervisor list # should be listed with a nonzero number of free VCPUs, RAM, and disk space
openstack hypervisor show [identifier]
openstack usage list
openstack quota show
```
