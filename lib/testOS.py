from fabric.api import *
IBM_OS = "system"

def os_test():
    env.shell = IBM_OS
    #run("CHGSYSVAL SYSVAL(QCMNRCYLMT) VALUE('2 5')")
    run("dspsysval qautovrt")
