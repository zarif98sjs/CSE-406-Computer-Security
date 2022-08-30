#include <linux/if_ether.h>
#include <linux/inet.h>
#include <linux/ip.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/tcp.h>
#include <linux/udp.h>

static struct nf_hook_ops hook1, hook2, hook3, hook4, hook5;

unsigned int printInfo(void *priv, struct sk_buff *skb, const struct nf_hook_state *state) {
    struct iphdr *iph;
    char *hook;
    char *protocol;

    switch (state->hook) {
        case NF_INET_LOCAL_IN:
            hook = "LOCAL_IN";
            break;
        case NF_INET_LOCAL_OUT:
            hook = "LOCAL_OUT";
            break;
        case NF_INET_PRE_ROUTING:
            hook = "PRE_ROUTING";
            break;
        case NF_INET_POST_ROUTING:
            hook = "POST_ROUTING";
            break;
        case NF_INET_FORWARD:
            hook = "FORWARD";
            break;
        default:
            hook = "IMPOSSIBLE";
            break;
    }
    printk(KERN_INFO "*** %s\n", hook);  // Print out the hook info

    iph = ip_hdr(skb);
    switch (iph->protocol) {
        case IPPROTO_UDP:
            protocol = "UDP";
            break;
        case IPPROTO_TCP:
            protocol = "TCP";
            break;
        case IPPROTO_ICMP:
            protocol = "ICMP";
            break;
        default:
            protocol = "OTHER";
            break;
    }
    // Print out the IP addresses and protocol
    printk(KERN_INFO "    %pI4  --> %pI4 (%s)\n", &(iph->saddr), &(iph->daddr), protocol);

    return NF_ACCEPT;
}

int registerFilter(void) {
    printk(KERN_INFO "Registering filters.\n");

    // NF_INET_PRE_ROUTING
    hook1.hook = printInfo;
    hook1.hooknum = NF_INET_PRE_ROUTING;
    hook1.pf = PF_INET;
    hook1.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook1);

    // NF_INET_LOCAL_IN
    hook2.hook = printInfo;
    hook2.hooknum = NF_INET_LOCAL_IN;
    hook2.pf = PF_INET;
    hook2.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook2);

    // NF_INET_FORWARD
    hook3.hook = printInfo;
    hook3.hooknum = NF_INET_FORWARD;
    hook3.pf = PF_INET;
    hook3.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook3);

    // NF_INET_LOCAL_OUT
    hook4.hook = printInfo;
    hook4.hooknum = NF_INET_LOCAL_OUT;
    hook4.pf = PF_INET;
    hook4.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook4);

    // NF_INET_POST_ROUTING
    hook5.hook = printInfo;
    hook5.hooknum = NF_INET_POST_ROUTING;
    hook5.pf = PF_INET;
    hook5.priority = NF_IP_PRI_FIRST;
    nf_register_net_hook(&init_net, &hook5);

    return 0;
}

void removeFilter(void) {
    printk(KERN_INFO "The filters are being removed.\n");
    nf_unregister_net_hook(&init_net, &hook1);
    nf_unregister_net_hook(&init_net, &hook2);
    nf_unregister_net_hook(&init_net, &hook3);
    nf_unregister_net_hook(&init_net, &hook4);
    nf_unregister_net_hook(&init_net, &hook5);
}

module_init(registerFilter);
module_exit(removeFilter);

MODULE_LICENSE("GPL");