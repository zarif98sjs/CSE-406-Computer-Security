#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>
#include <linux/icmp.h>
#include <linux/if_ether.h>
#include <linux/inet.h>

static struct nf_hook_ops hook1, hook2; 
//static FILE *fptr;
int count[5]={0,0,0,0,0};
int i;
//0->10..1
//1->10..5
//2->10..11
//3->192..6
//4->192..7

unsigned int blockICMP(void *priv, struct sk_buff *skb,
                       const struct nf_hook_state *state)
{
int k;
for(k=0;k<5;k++)
	printk(KERN_INFO "*** COUNT %d %d\n",k,count[k]);

   struct iphdr *iph;
   struct icmphdr *icmph;
   u32  src_ip_addr[5];
   int j;

   char ip[16] = "192.168.60.5";
   
   char ip0[16] = "10.9.0.5";
   char ip1[16] = "10.9.0.1";
   char ip2[16] = "10.9.0.11";
   char ip3[16] = "192.168.60.6";
   char ip4[16] = "192.168.60.7";
   
   in4_pton(ip0, -1, (u8 *)&src_ip_addr[0], '\0', NULL);
   in4_pton(ip1, -1, (u8 *)&src_ip_addr[1], '\0', NULL);
   in4_pton(ip2, -1, (u8 *)&src_ip_addr[2], '\0', NULL);
   in4_pton(ip3, -1, (u8 *)&src_ip_addr[3], '\0', NULL);
   in4_pton(ip4, -1, (u8 *)&src_ip_addr[4], '\0', NULL);
   
   printk(KERN_WARNING "*** src ip address", &(src_ip_addr));
   printk(KERN_WARNING "*** src ip address", &(src_ip_addr)+1);
   printk(KERN_WARNING "*** src ip address", &(src_ip_addr)+2);
   printk(KERN_WARNING "*** src ip address", &(src_ip_addr)+3);
   printk(KERN_WARNING "*** src ip address", &(src_ip_addr)+4);
   
   u32  ip_addr;

   if (!skb) return NF_ACCEPT;

   iph = ip_hdr(skb);
   // Convert the IPv4 address from dotted decimal to 32-bit binary
   in4_pton(ip, -1, (u8 *)&ip_addr, '\0', NULL);
	printk(KERN_WARNING "*** des ip address %pI4", &iph->daddr);
   if (iph->protocol == IPPROTO_ICMP) {
       icmph = icmp_hdr(skb);
       if (iph->daddr == ip_addr && icmph->type == ICMP_ECHO){
       	 //fscanf(fptr,"%d", &count);
       	 printk(KERN_WARNING "*** CONDITION MATCHES 1");
       	 for (j=0;j<5;j++)
       	 {
       	 
       	 	if(iph->saddr == src_ip_addr[j])
       	 	{
       	 	printk(KERN_WARNING "*** CONDITION MATCHES");
       	 	
	       	 	if(count[j]>5)
		       	 {
		       	 	printk(KERN_WARNING "*** Dropping %pI4 (ICMP)\n", &(iph->daddr));
			    		return NF_DROP;
		       	 }
		       	 else
		       	 {
		       	 	count[j] = count[j]+1 ;
		       	 	//fprintf(fptr,"%d",count);
		       	 }
	       	 	break;
       	 	}
       	 }
       	 
       	 
       	 
            
        }
   }
   return NF_ACCEPT;
}


unsigned int printInfo(void *priv, struct sk_buff *skb,
                 const struct nf_hook_state *state)
{
   struct iphdr *iph;
   char *hook;
   char *protocol;

   switch (state->hook){
     case NF_INET_LOCAL_IN:     hook = "LOCAL_IN";     break; 
     case NF_INET_LOCAL_OUT:    hook = "LOCAL_OUT";    break; 
     case NF_INET_PRE_ROUTING:  hook = "PRE_ROUTING";  break; 
     case NF_INET_POST_ROUTING: hook = "POST_ROUTING"; break; 
     case NF_INET_FORWARD:      hook = "FORWARD";      break; 
     default:                   hook = "IMPOSSIBLE";   break;
   }
   printk(KERN_INFO "*** %s\n", hook); // Print out the hook info

   iph = ip_hdr(skb);
   switch (iph->protocol){
     case IPPROTO_UDP:  protocol = "UDP";   break;
     case IPPROTO_TCP:  protocol = "TCP";   break;
     case IPPROTO_ICMP: protocol = "ICMP";  break;
     default:           protocol = "OTHER"; break;

   }
   // Print out the IP addresses and protocol
   printk(KERN_INFO "    %pI4  --> %pI4 (%s)\n", 
                    &(iph->saddr), &(iph->daddr), protocol);

   return NF_ACCEPT;
}


int registerFilter(void) {
   printk(KERN_INFO "Registering filters.\n");
   //fopen("//home//seed//Firewall//Labsetup//Files/packet_filter_online//count.txt","w");
   //fprintk(fptr,"%d",count);

   hook1.hook = printInfo;
   hook1.hooknum = NF_INET_LOCAL_OUT;
   hook1.pf = PF_INET;
   hook1.priority = NF_IP_PRI_FIRST;
   nf_register_net_hook(&init_net, &hook1);
   
   hook2.hook = blockICMP;
   hook2.hooknum = NF_INET_PRE_ROUTING;
   hook2.pf = PF_INET;
   hook2.priority = NF_IP_PRI_FIRST;
   nf_register_net_hook(&init_net, &hook2);

   return 0;
}

void removeFilter(void) {
   printk(KERN_INFO "The filters are being removed.\n");
   nf_unregister_net_hook(&init_net, &hook1);
   nf_unregister_net_hook(&init_net, &hook2);
   //fclose(fptr);
}

module_init(registerFilter);
module_exit(removeFilter);

MODULE_LICENSE("GPL");
