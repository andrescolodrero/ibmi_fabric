from fabric.api import *
import config  as config
# Insert this 2 values for testing
#env.key_filename = '../id_rsa.pub'
#env.user = "acl"
def os_test():
    env.shell = "system"
    #run("CHGSYSVAL SYSVAL(QCMNRCYLMT) VALUE('2 5')")
    run("dspsysval qautovrt")
