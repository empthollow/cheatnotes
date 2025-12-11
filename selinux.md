# Basic Functions
get status of selinux
```bash
getenforce				get status
```
set enforcement status
```bash
setenforce				set enforcement status
```
view selinux contexts
```bash
ls -Z					view selinux contexts
```
restore selinux permissions
```bash
restorecon [path]			restore selinux permissions after file operations
```
restore selinux directory permissions
```bash
restorecon -rv
```

# Viewing Logs
show all longs
```bash
sealert -a /var/log/audit/audit.log	show all logs
```
show specific alert details
```bash
sealert -l [#]				show specific alert details
```
audit search / show logs and filter recent
```bash
ausearch -m AVC -ts recent
```
see logs interactively
```bash
journalctl -t setroubleshoot		see logs interactively
```

