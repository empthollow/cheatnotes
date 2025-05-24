```bash
#/bin/bash

if [ "$(id -u)" != "0"]; then
	echo "you are not root"
	exit
fi

dnf -y install podman podman-compose redir vim
echo "[Unit]
Description=Redirect tcp port 80 to 8080 with redir

[Service]
ExecStart=/bin/redir -sn :80 127.0.0.1:8080

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/redir80.service
systemctl enable --now redir80.service
```