# Isolate Bash Process

```bash
sudo unshare --fork --pid --mount-proc bash
sudo unshare --fork --pid --net --mount-proc bash
```

# Skopeo Commands

```bash
skopeo inspect --format "{{.RepoTags}}" docker://docker.io/library/ubuntu:latest | tr ' ' '\n' | grep focal
skopeo inspect docker://docker.io/ubuntu/apache2
```

# Podman Commands

## Container Management

```bash
podman container prune  # delete non-running containers
--rm  # delete containers on stop
-it  # interactive tty
--hostname  # internal to container
-d  # detach
podman container attach NAME
-exit will stop the container
-to exit ctrl+p ctrl+q

## Monitoring

```bash
podman container top NAME
podman container inspect NAME
podman container logs NAME
podman container inspect --format "{{.Config.Cmd}}"  # check default command
podman container exec -it NAME /bin/bash
podman rm -f NAME  # delete running container
```

# SELinux for WWW Dir

```bash
chcon -Rt container_file_t DIR
```

# Create Systemd File

```bash
podman generate systemd NAME
systemctl enable --now NAME
systemctl daemon-reload
```

# Set Boolean for Running Systemd Inside a Container

```bash
sudo setsebool -P container_manage_cgroup true
```

# Creating Container

```bash
mkdir -p ~project/fedora
ssh-keygen -f FILE -N ""
cp ~/.ssh/FILE.pub
echo "tux ALL=(root) NOPASSWD: ALL" . tux
visudo -cf project/fedora/tux
vim Dockerfile
```

## Dockerfile Example

```dockerfile
FROM = docker image
RUN = execute command such as install packages
RUN = execute another command
RUN example user create = useradd -m tux -G wheel && echo 'tux:[Password1]' | chpasswd
COPY = copy file into container; example = COPY --chmod=600 tux /etc/sudoers.d/tux
EXAMPLE SSH KEY = COPY --chmod=700 --chown=tux:tux KEY.pub /home/tux/.ssh/authorized_keys
EXPOSE = expose port # through firewall; each container has its own firewall
CMD ["/usr/sbin/init"] = is symbolic link to systemd in fedora38; default executable
```

## Build Image

```bash
podman image build -t NAME .
```

# Prevent SSH from Adding to KnownHosts File

```bash
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 2222:22 tux@localhost
```

# Podman Network Commands

```bash
podman network ls
podman network create NAME --subnet SUBNET/xx --gateway GATEWAYIP
podman container run -d name NAME --hostname HOSTNAME -p XXXX:XX --network NAME CONTAINERIMAGE
```

# Podman System Prune

```bash
podman system prune  # delete unused containers
podman system prune -a -f  # delete all unused networks containers etc
