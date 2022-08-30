#include <linux/kernel.h>
#include <linux/module.h>

int initialization(void) {
    printk(KERN_INFO "Hello World!\n");
    return 0;
}

void cleanup(void) { printk(KERN_INFO "Bye-bye World!.\n"); }

module_init(initialization);
module_exit(cleanup);

MODULE_LICENSE("GPL");
