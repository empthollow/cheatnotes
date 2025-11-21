# CREATE AND INSTALL ISO TO NEW VM
*Always run as root*
```bash
sudo virt-install --reinstall arch-proto --os-variant archlinux --memory 4096 --vcpus 2 --disk size=20 --location /downloads/archlinux-2023.09.01-x86_64.iso,initrd=/arch/boot/x86_64/initramfs-linux.img,kernel='/arch/boot/x86_64/vmlinuz-linux' --graphics none --extra-args 'console=tty0 console=ttyS0,115200n8 --- console=tty0 console=ttyS0,115200n8 archisolabel=ARCH_202309' --console pty,target_type=serial --tpm model='tpm-tis',type=emulator,version='2.0'
```

# SERIAL OPTIONS
```bash
--nographics --extra-args console=ttyS0
```

# LIST VMS
```bash
virsh list
virsh list --all
```

# LIST VOLUMES / DISKS
```bash
virsh vol-list --pool default --detail
```

# SHOW SYS INFO FOR VM
```bash
virsh dominfo [vm-name]
```

# AUTOSTART VM
```bash
virsh autostart [vm-name]
virsh autostart --disable [vm-name]
```

# CREATE DISK IMAGE
```bash
qemu-img create -f qcow2 [foobar].qcow2 [size]
qemu-img resize /path/to/your.qcow2 +new_size
```

# CHANGE MAX LOCKED MEM FOR MEM ERRORS
```bash
cat /proc/sys/vm/overcommit_memory
sudo sysctl -w vm.overcommit_memory=1
echo "vm.overcommit_memory=1" | sudo tee -a /etc/sysctl.conf
```

```bash
ulimit -l # max mem locked
ulimit -a # list all limits
echo "* soft memlock unlimited" | sudo tee -a /etc/security/limits.conf
echo "* hard memlock unlimited" | sudo tee -a /etc/security/limits.conf
```

# RESTART LIBVIRT
```bash
sudo systemctl restart libvirtd
sudo systemctl restart virtqemud
```
