# Basic Functions
```bash
getenforce				get status
setenforce				set enforcement status
ls -Z					view selinux contexts
restorecon [path]			restore selinux permissions after file operations
```

# Viewing Logs

```bash
sealert -a /var/log/audit/audit.log	show all logs
sealert -l [#]				show specific alert details
ausearch -m AVC,USER_AVC -ts recent	show logs and filter recent
journalctl -t setroubleshoot		see logs interactively
```