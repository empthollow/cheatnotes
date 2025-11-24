# ssh syntax
Connect to a remote server with SSH, disabling strict host key checking.  
```bash
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 2222:22 tux@host
```

Use only the specified key to avoid 'too many login failures'
```bash
ssh -o IdentityOnly=yes -i [.ssh/keyname] [user@host]
```

Create an SSH key of specified type (e.g., `ed25519`) and save to a file. 
```bash
ssh-keygen -t [ed25519] -f [filename]
```

Remove a host from the known hosts file.  
```bash
ssh-keygen -R [host]
```

Copy your public SSH key to a remote host for password-less login.  
```bash
ssh-copy-id -i [identity file] [user@host]
```
or
```bash
cat [~/.ssh/id_*.pub] | ssh [user@host] "tee -a ~/.ssh/authorized_keys > /dev/null"
```

Add a key to the SSH authentication agent (keyring).  
```bash
ssh-add [key file]
```

# tmux
Detach from the current tmux session.  
```bash
ctrl+b d
```

List all active tmux sessions.  
```bash
tmux list-sessions
```

Attach to a specific tmux session by ID.  
```bash
tmux attach-session -t [#]
```

Open the window menu.  
```bash
ctrl+b <
```

Rename the current tmux session.  
```bash
ctrl+b $
```

List all tmux key bindings.  
```bash
ctrl+b ?
```

Split the window horizontally.  
```bash
ctrl+b "
```

Split the window vertically.  
```bash
ctrl+b %
```

Select the pane in the specified direction.  
```bash
ctrl+b [arrow]
```

Resize the pane by 5 lines or columns.  
```bash
ctrl+b alt+[arrow]
```

Kill the current tmux window.  
```bash
ctrl+b &
```

Create a new tmux window.  
```bash
ctrl+b c
```

Switch to the tmux window by its number.  
```bash
ctrl+b [#]
```

Choose a window or session from a list.  
```bash
ctrl+b w
```

# vim
Reload syntax highlighting.  
```bash
:syntax sync fromstart
```

Find and replace all instances in the document.  
```bash
:%s/[search]/[replace]/g
```

Insert text above the line containing the search text.  
```bash
:%g/[search]/exe "normal Otxt"
```

Change the syntax highlighting theme.  
```bash
:colorscheme [theme]
```

Enable word wrap.  
```bash
:set wrap
```

Disable word wrap.  
```bash
:set nowrap
```

Toggle word wrap.  
```bash
:set wrap! or :set nowrap!
```

Show the detected file type for syntax highlighting.  
```bash
:set filetype?
```

Set the file type for syntax highlighting.  
```bash
:set filetype=[type]
```

Show hidden characters like line endings.  
```bash
:set list
```

Hide line endings.  
```bash
:set nolist
```

# journalctl
Show the last 10 entries from the system journal.  
```bash
journalctl -n
```

Show the last 15 entries from the system journal.  
```bash
journalctl -n [15]
```

Follow the log file in real-time.  
```bash
journalctl -f
```

Show logs for a specific systemd unit.  
```bash
journalctl -u [systemd unit]
```

Show logs starting from a specific date and time.  
```bash
journalctl --since [2025-03-28 12:00:00]
```

Show logs up until a specified time.  
```bash
journalctl --until
```

List available boot logs.  
```bash
journalctl --list-boots
```

Show logs from the current boot.  
```bash
journalctl -b
```

Show logs from a specific boot by ID.  
```bash
journalctl -b [id from list]
```

View the end of the log.  
```bash
journalctl -e
```

# Network tools
Ping a target from a specific source IP.  
```bash
ping -I 172.22.2.2 8.8.8.8
```

Trace the route from a specific source IP.  
```bash
traceroute -s 172.22.2.2 8.8.8.8
```

Show DNS information.  
```bash
resolvctl
```

Show DNS resolver status.  
```bash
systemd-resolve --status
```

Perform DNS server lookup.  
```bash
nslookup
```

Perform a detailed DNS query.  
```bash
dig
```

Dump TCP packets on a specified interface with filters.  
```bash
tcpdump -i <iface> [icmp | port #]
```

Display the system's routing table.  
```bash
route
```

Show the routing table.  
```bash
netstat -r
```

Show the process listening on a specific port.  
```bash
lsof -i :[port #]
```

## IP Command
Show the system’s routing tables.  
```bash
ip route show
```

Show routes for a specific routing table.  
```bash
ip route show table <table name>
```

Show all available routing tables.  
```bash
ip route show table all
```

Show the route to a specific IP address.  
```bash
ip route get [IP]
```

Show neighbors (ARP cache).  
```bash
ip neigh show
```

## bridge command
Check attached interfaces
```bash
bridge link show 
```

Use bridge to check attached vlans
```bash
bridge vlan show
```

View forwarding database
```bash
bridge fdb show
```

## Kernel routing and options 
Defines custom routing tables.  
```bash
/etc/iproute2/rt_tables
```

Enable or disable IP forwarding.  
```bash
/proc/sys/net/ipv4/ip_forward/
```

ViewEnable Disable Vlan Filtering
```bash
cat /sys/class/net/bridge-vlan10/bridge/vlan_filtering
```

Enable or disable reverse path filtering on an interface.  
```bash
cat /proc/sys/net/ipv4/conf/<interface_name>/rp_filter
```

Configuration file for kernel settings persistence, including IP forwarding.  
```bash
/etc/sysctl.conf
```

Check or modify reverse path filtering.  
```bash
sysctl net.ipv4.conf.<all>.rp_filter
```

## Network Manager
create / mod connection profile
```bash 
nmcli con [ add | mod ] type [ ethernet | bridge | port | ovs-bridge | ovs-interface | ovs-port | ovs-patch ] ifname [ link ] con-name [ name ] ipv4.method [ disabled | manual | auto ]  ipv6.method [ disabled | manual | auto ] connection.autoconnect [ yes | no ] ipv4.address [ xxx.xxx.xxx.xxx/xx ] ipv6.address [ FFFf:FFFF:FFFF:FFFF:FFFF:FFFF ] 
```

create bridge
```bash
nmcli con add type bridge con-name [ BRIDGE_PROFILE ] ifname [ BRIDGE_NAME ]
```

### Other Settings

Disable auto-added routes in NetworkManager.  
```bash
nmcli con option: ipv4.ignore-auto-routes yes
```

Ensure default route is not automatically added.  
```bash
nmcli con option: ipv4.never-default yes
```

## OpenVswitch
view ovs configuration
```bash
ovs-vsctl show
```
create a local switch / ovs bridge which functions as a switch
```bash
ovs-vsctl add-br [ BRIDGE_NAME ]
ovs-vsctl add-port [ BRIDGE_NAME ] [ PORT_NAME or DEV ] 
```
this can be done with network manager for persistence NOTE: requies ovs plugin
it's often best practice to define an intermediate "OVS Port" connection profile before adding the actual interface. this maps the NM profiles to ovs elements being created.

```bash
nmcli connection add type ovs-bridge con-name [ PROFILE_NAME ] ifname [ BRIDGE_NAME ]
nmcli connection add type ovs-port conn.interface [ PROFILE_NAME ] master [ PROFILE_NAME ]
nmcli connection add type ethernet conn.interface [ PROFILE_NAME ] master [ PROFILE_NAME ]
# latest
nmcli con add con-name brovs type ovs-bridge ifname bridge-ovs
nmcli con add con-name ovs-port type ovs-port ifname ovs-port master brovs
nmcli con add con-name ovs-dev type ethernet ifname eno4 master ovs-port
nmcli con mod brovs ipv4.method manual ipv4.addresses 172.22.1.2/24 ipv4.gateway 172.22.1.1 ipv4.dns 192.168.1.50
```

# flatpak
View installed Flatpak packages.  
```bash
flatpak list
```

View application IDs and runtime dependencies.  
```bash
flatpak list --app --columns=application,runtime
```

Remove unused Flatpak packages.  
```bash
flatpak remove --unused
```

List available updates for Flatpak apps.  
```bash
flatpak remote-ls --updates
```

Give Flatpak application access to a specific filesystem path.  
```bash
flatpak override <package ID> --filesystem=</path/>
```

List Flatpak installation paths.  
```bash
flatpak --installations
```

Kill a running Flatpak application.  
```bash
flatpak kill
```

Show detailed information about a Flatpak application.  
```bash
flatpak info
```

# firewall-cmd
List all open ports in the firewall.  
```bash
firewall-cmd --list-ports
```

Add a port to the firewall permanently.  
```bash
firewall-cmd --add-port=[PORT]/[tcp|udp] --permanent
```

Reload the firewall configuration.  
```bash
firewall-cmd --reload
```

Display all firewall settings.  
```bash
firewall-cmd --list-all
```

# disk operations
View partitions, volumes, and their filesystem types.  
```bash
df -T
```

View partitions and free space in human-readable format.  
```bash
df -h
```

View block device information including filesystem type.  
```bash
lsblk -f
```

Show block device information, including filesystem type and UUID.  
```bash
blkid
```

Create a filesystem on a partition or volume.  
```bash
mkfs.[fs]
```

Force a filesystem check for ext filesystems.  
```bash
e2fsck -f
```

Check and repair filesystems.  
```bash
fsck
```

Resize an ext filesystem.  
```bash
resize2fs [partition or logical volume] [size]
```

Repair an XFS filesystem.  
```bash
xfs_repair [device path]
```

Check an XFS filesystem without making changes.  
```bash
xfs_repair -n [device path]
```

Grow an XFS filesystem to fill the partition or volume.  
```bash
xfs_growfs [dev path]
```

# Volumes
## LVM
Display information about a physical volume.  
```bash
pvdisplay [optional pv name]
```

Display information about a volume group.  
```bash
vgdisplay [optional vol group name]
```

Display information about a logical volume.  
```bash
lvdisplay [optional logical vol name]
```

Extend a logical volume to a new size or by an increment.  
```bash
lvextend -L [total-new-size | +add-size]
```

Create a new logical volume in a volume group.  
```bash
lvcreate -L [size] -n [new_lv_name] [vg_name]
```

Create a logical volume using all remaining space in a volume group.  
```bash
lvcreate -l 100%FREE -n [new_lv_name] [vg_name]
```

Delete a logical volume.  
```bash
lvremove [device path]
```

Display information about all logical volumes.  
```bash
lvs
```

## mount
```bash
mount -t cifs [//server/share] [mount point] -o credentials=[file path],uid=[1000],gid=[1000],file_mode=0644,dir_mode=0755
```
creds file format
```bash
username=[name]
password=[pass]
domain=[optional domain]
```
credentials can be put on cli
```bash
user=[user],pass=[pass]
```

# tar
Create an archive, excluding a subpath and changing directory before adding content.  
```bash
tar -czvf [name].tar.gz --exclude=[relative path] -C [path] .
```

Extract the archive contents to a specific location.  
```bash
tar xpzf [name].tar.gz -C [path to extract]

### process handling
#### background process persistence when shell exit
```bash
nohup [command] &
```

# rsync
a: archive opt preserves file attributes and sym links
v: verbose
P: progress & partial file handling
--info=progress2 rsync shows overall transfer progress (aggregate bytes transferred vs total)
```bash
rsync -av[P | --info=progress2 --partial ] [source] [destination - local or ssh supported]
```

# Package Management
## Red Hat
openvswitch package
```bash
subscription-manager repos --enable=fast-datapath-for-rhel-9-x86_64-rpms
```
