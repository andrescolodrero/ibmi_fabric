from fabric.api import *
IBM_OS = "system"

def set_security_values():
    run("CHGSYSVAL SYSVAL(QPWDEXPITV) VALUE('90')")
    run("CHGSYSVAL SYSVAL(QPWDLMTREP) VALUE('2')")
    # bASIC AND OLD SEC SETTINGS. NON-SECURE
    run("CHGSYSVAL SYSVAL(QPWDMAXLEN) VALUE('10')")
    run("CHGSYSVAL SYSVAL(QPWDMINLEN) VALUE('5')")
    run("CHGSYSVAL SYSVAL(QPWDRQDDIF) VALUE('7')")
    # Necesary for PowerHA
    run("CHGSYSVAL SYSVAL(QRETSVRSEC) VALUE('1')")
    # and the most important
    run("CHGSYSVAL SYSVAL(QSECURITY) VALUE('30')")
    #run("CHGSYSVAL SYSVAL(QSECURITY) VALUE('40')")
    # more jobqentryes in qbatch
    run('CHGJOBQE SBSD(QSYS/QBATCH) JOBQ(QGPL/QBATCH) MAXACT(*NOMAX)')

def get_system_values():
    print("test")
    # To-DO for checkings