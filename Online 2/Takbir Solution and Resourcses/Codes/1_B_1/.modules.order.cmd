cmd_/home/seed/Desktop/Firewall_Practice/1_B/modules.order := {   echo /home/seed/Desktop/Firewall_Practice/1_B/my_simple_firewall.ko; :; } | awk '!x[$$0]++' - > /home/seed/Desktop/Firewall_Practice/1_B/modules.order