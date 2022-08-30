For the genjam at the ending: 
Only flushing iptable doesn't work. "iptables -P FORWARD ACCEPT" -> after this worked fine

ALternatively, you can just restart the docker container.

docker restart <container-id>

this removes the modified iptable as well.