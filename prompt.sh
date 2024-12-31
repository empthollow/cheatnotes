#/bin/bash
# place in /etc/profile.d/
# delete irrelevant themes 

# physical server theme
if [ "$(id -u)" == "0" ] ; then
	PS1='\[\e[1;31m\]\u\[\e[1;32m\]@\h\[\e[1;31m\] \W \$\[\e[m\] '
else
	PS1="\[\e[1;33m\]\u\[\e[1;32m\]@\h \[\e[1;32m\]\W \$\[\e[m\] "
fi

# VM theme 
if [ "$(id -u)" == "0" ] ; then
        PS1='\[\e[1;31m\]\u\[\e[1;33m\]@\h\[\e[1;33m\] \W \$\[\e[1;33m\] '
else
        PS1="\[\e[1;35m\]\u\[\e[1;33m\]@\h \[\e[1;33m\]\W \$\[\e[1;33m\] "
fi

# workstation theme
if [ "$(id -u)" == "0" ] ; then
	PS1='\[\e[1;31m\]\u\[\e[1;32m\]@\h\[\e[1;31m\] \W \$\[\e[m\] '
else
	PS1="\[\e[1;33m\]\u\[\e[1;34m\]@\h\[\e[1;33m\] \W \$\[\e[m\] "
fi
