# Help
Help for all commands
```bash
openstack help [command]
openstack help [server create] 
```
Universal view commands
- These will be shown in sections but know they can be used with nearly all assets
```bash
# view list of assets
openstack SERVICE list
# show details about asset
openstack SERIVCE show
```
For many commands there are flags to format output
```bash
# if experiencing problems viewing in window
--fit-width 
# view in different format choose from 'csv', 'json', 'table', 'value', 'yaml'
## value can will show only the field value which can be useful for copy or scripting
-f [yaml | json | value] 
# View additional info not default in table
--long 
# show a column or columns
## also works for values in 'openstack server show SERVER_NAME'
-c FIELD_NAME
```
# Nova
## Server creation and management
Create server / VM
```bash
openstack server create --name [image_name or ID] SERVER_NAME 
```
Create with a cd-rom drive
```bash
openstack server create --config-drive=true
```
Typical create VM command
```bash
openstack server create \
  --flavor m1.small \
  --image cirros62 \
  --key-name KEY_NAME \
  --security-group GROUP_NAME \
  --network NETWORK_NAME \
  VM_NAME
```
Specify user data file
- Will execute a script or cloud config file upon server creation
```bash
openstack server create	--user-data [ SCRIPT.sh | CLOUD_CONFIG.yaml ] SERVER_NAME
```
Modify server command examples
```bash
openstack server add security group SERVER_NAME SECGROUP
openstack server remove security group SERVER_NAME SECGROUP
openstack server add floating ip SERVER_NAME FLOATING_IP
openstack server remove floating ip SERVER_NAME FLOATING_IP
```
Show url to access server shell console
```bash
openstack console url show SERVER_NAME
```
Show logs such as when booting
```bash
openstack console log show SERVER_NAME
```
Display server information and status
```bash
openstack server show SERVER_NAME
```
Server / VM control commands
```bash
openstack server stop SERVER_NAME
openstack server start SERVER_NAME
openstack server delete SERVER_NAME 
```
Resize a VM
```bash
openstack resize --flavor [ m1.large ] SERVER_NAME
```
Resize needs to be confirmed or reverted
```bash
openstack server resize confirm SERVER_NAME
openstack server resize revert SERVER_NAME
```
## VM flavors
Create VM flavor example
```bash
openstack flavor create [ --ram 512 --disk 5 --vcpus 1 --public m1.tiny ]
```
List VM flavors
```bash
openstack flavor list
```
## SSH Key Pairs
Create a keypair
```bash
openstack keypair create KEY_NAME > KEY.pem
chmod 600 key.pem
```
Add own key
```bash
openstack keypair create --public-key KEY.pub 
```
View keys
```bash
openstack keypair list
openstack keypair show KEY_NAME
openstack keypair show --public-key KEY_NAME
```
## Nova management
List parts of nova 
- Requires admin
```bash
openstack compute service list 
nova compute service list --service [nova-compute or other]
```
View hypervisor nodes
```bash
openstack hypervisor list 
```
Show details on specific hypervisor
```bash
openstack hypervisor show [identifier]
```
Show total usage
```bash
openstack usage list
```
Show project quotas
```bash
openstack quota show
```
Set quotas
```bash
openstack quote set [flag] XX PROJECT_NAME
```
Quota flags
```bash
--backup-gigabytes      --injected-file-size    --routers
--backups               --injected-path-size    --secgroup-rules
--check-limit           --instances             --secgroups
--class                 --key-pairs             --server-group-members
--cores                 --networks              --server-groups
--fixed-ips             --no-force              --snapshots
--floating-ips          --per-volume-gigabytes  --subnetpools
--force                 --ports                 --subnets
--gigabytes             --properties            --volumes
--help                  --ram                   --volume-type
--injected-files        --rbac-policies
```
# Neutron / Networking
## Network Management
List networks
```bash
openstack network list
```
View details on a specific network
```bash
openstack network show NETWORK_NAME
```
View network agents and health
```bash
openstack network agent list
```
View provider (external) network details
```bash
openstack network service provider list
```
## Network creation
Create a network
```bash
openstack network create NETWORK_NAME
```
Create external (to openstack) network
Often named provider or public
```bash
openstack network create \
--external \
--provider-network-type [flat] \
--provider-physical-network NETWORK_NAME_DEFINED_IN_NEUTRON_CONFIG
```
Rename a network
```bash
openstack network set --name OLD NEW
```
## Subnets 
Create subnet
- Host route is like a static route and not necessary for simple configurations
- DNS is configured on Subnets
- Typically subnet is NETWORK_NAME-subnet
```bash
openstack subnet create NETWORK_NAME-subnet \
  --network NETWORK_NAME \
  --subnet-range [10.10.1.0/24] \
  --dns-nameserver [8.8.8.8] \
  --host-route destination=192.168.50.0/24,gateway=10.10.1.254
```
Create external subnet
- For external network, for flat, openstack subnet must match physical iface subnet
  - May be a smaller mask within the physical interface subnet
```bash
openstack subnet create \
--network [external network name]  \
--subnet-range [203.0.113.0/24] \
--gateway [physical router IP]  \
--allocation-pool start=[ipv4 least start],end=[ipv4 lease end] \
--dns-nameserver [8.8.8.8] [public-subnet-name]
```
# Routers
Create router and add subnet(s)
- Multiple subnets can be added
- A port may be automatically added
  - A port is sometimes required to be manually added and subnet IP assigned
    - This is typically the 2nd port on a subnet
```bash
openstack router create ROUTER_NAME
openstack router add subnet ROUTER_NAME SUBNET_NAME
openstack router add port PORT_NAME ROUTER_NAME
```
Create a port
```bash
openstack port create PORT_NAME --network NETWORK_NAME
```
Create external router
- External routers created as admin can be used across all projects
  - Project subnets will need to be attached by admin
  - The router will automatically get and IP and be treaded as static
- Router should be created and then do the following to set it up as external
```bash
openstack router set ROUTER_NAME --external-gateway EXTERNAL_NETWORK_NAME
```
Additional options common when using two external networks
```bash
# Traffic leaving the router will keep the internal private IP of the VM
--disable-snat 
# Manually set IP
--fixed-ip
# Equal-Cost Multi-Path, enables load balancing
--enable-default-route-ecmp 
# Bidirectional Forwarding Detection, high-speed "heartbeat" check
--enable-default-route-bfd
```
# Floating IP
Management commands
- Self explanitory
```bash
openstack floating ip create EXTERNAL_NETWORK_NAME
openstack floating ip delete IP_ADDR
openstack floating ip list
```
## Security Groups
Create security group
- Group must be created and rule added as a second operation
```bash
openstack security group create NAME
openstack security group rule create --dst-port XX --protocol NAME
```

```bash
openstack security group list 
```
long shows direction
```bash
openstack security group rule list NAME --long
```
## OpenVSwitch
### Configuration and create commands
- A minimal manual setup is required for neutron-ovs-agent to properly interact
Minimal Setup
```bash
Bridge br-ex - [ip_address]
    Port [for_eth1]
        Interface [eth1]
Bridge br-int
```
Create bridges
```bash
ovs-vsctl --may-exist add-br br-int
ovs-vsctl --may-exist add-br br-ex
```
Create port for external network
```bash
ovs-vsctl --may-exist add-port br-ex [eth1]
```
### OVS commands for viewing configuration
OpenVSwitch list of bridges
```bash
ovs-vsctl show 
```
List bridges
```bash
ovs-vsctl list-br 
```
List config db for open vSwitch
```bash
ovs-vsctl list Open_vSwitch 
```
Checks / shows openflow rules
```bash
ovs-ofctl dump-flows [br-tun]
```
Show known mac addresses
```bash
ovs-appctl fdb/show [br-enp2s0] 
```
# Projects, Users, Roles 
- User Must Have Project to Log In
  - The exception is admin when using RBAC
Create project
```bash
openstack project create --domain DOMAIN_NAME --description "[description]" PROJECT_NAME
```
Create user
```bash
openstack user create --domain DOMAIN_NAME --password PASSWORD USERNAME
```
Add role 
- Connect user and project
```bash
openstack role add --project [project name] --user [username] [role]
```
List all roles in openstack
```bash
openstack role list 
```
Roles assigned to user
```bash
openstack role assignment list --user [user_name] --project [project_name] --names 
```
List users & roles in a project
```bash
openstack role assignment list --project [project_name] --names 
```
# Glance
Create image
```bash
openstack image create --disk-format qcow2 --container-format bare --public --file PATH_TO_IMAGE GLANCE_IMAGE_NAME
```
List images
```bash
openstack image list
```
Check if image is accessible and available
```bash
openstack image show IMAGE_NAME
```
Download image from glance
```bash
openstack image save --file DESTINATION_FILE IMAGE_NAME
```
# Cinder
View volumes
```bash
openstack volume list
```
Show volume details
```bash
openstack volume show VOLUME_NAME
```
Show cinder services
```bash
openstack volume service list
```
View volume pools
```bash
openstack volume backend pool list
```
# Managing Openstack
View service endpoints
```bash
openstack endpoint list
openstack endpoint list --service SERVICE NAME
```








