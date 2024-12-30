#/bin/bash
# place in /etc/profile.d/
if [ "$(id -u)" == "0" ] ; then
	PS1='\[\e[1;31m\]\u\[\e[1;32m\]@\h\[\e[1;32m\] \W \$\[\e[m\] '
else
	PS1="\[\e[1;33m\]\u\[\e[1;32m\]@\h \[\e[1;32m\]\W \$\[\e[m\] "
fi
