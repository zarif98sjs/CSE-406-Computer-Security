cmd_/home/seed/Desktop/Firewall_Practice/1_B/Module.symvers := sed 's/\.ko$$/\.o/' /home/seed/Desktop/Firewall_Practice/1_B/modules.order | scripts/mod/modpost -m -a  -o /home/seed/Desktop/Firewall_Practice/1_B/Module.symvers -e -i Module.symvers   -T -