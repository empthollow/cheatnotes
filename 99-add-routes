#!/bin/bash

# place in /etc/NetworkManager/dispatcher.d/
# give execute permissions
# Check if the interface is up and apply routing rules accordingly
if [ "$2" == "up" ]; then
  case "$1" in
    # For bridge0 interface
    bridge0)
      # Add routing rule and routes for bridge0
      ip route add default via 192.168.1.1 dev bridge0
      ip rule add priority 100 from 192.168.1.60 lookup bridge0_table
      ip route add 192.168.1.1 dev bridge0
      ip route add default via 192.168.1.1 dev bridge0 table bridge0_table
      ;;
    # For bridge-knet interface
    bridge-knet)
      # Add routing rule and routes for bridge-knet
      ip rule add priority 110 from 172.22.3.2 lookup bridge-knet_table
      ip route add 172.22.3.1 dev bridge-knet
      ip route add default via 172.22.3.1 dev bridge-knet table bridge-knet_table
      ;;
    # For bridge-serv interface
    bridge-serv)
      # Add routing rule and routes for bridge-serv
      ip rule add priority 120 from 172.22.2.2 lookup bridge-serv_table
      ip route add 172.22.2.1 dev bridge-serv
      ip route add default via 172.22.2.1 dev bridge-serv table bridge-serv_table
      ;;
  esac
fi

