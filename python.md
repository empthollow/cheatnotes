# Python bash commands
## PRINT PYTHONPATH
```bash
python3 -c "import sys; print(sys.path)"
```
## EXPORT PATH
```bash
export PYTHONPATH=/usr/share/openstack-dashboard:$PYTHONPATH
```
## IMPORT MODULE
```bash
python3 -c "import [openstack_dashboard]"
```
```sh
# List all installed packages:
python3 -m pip list

# Show outdated packages:
python3 -m pip list --outdated

# Show packages with versions in freeze format (suitable for requirements.txt):
python3 -m pip freeze

# Show detailed info for a single package:
python3 -m pip show <package-name>

# Search installed packages by name (example finds "requests"):
python3 -m pip list | grep -i requests
# (On Windows PowerShell use: python3 -m pip list | Select-String -Pattern "requests")

# List packages in a virtual environment: activate the venv first, then run
python -m pip list
# (or use the venv's python path directly)

