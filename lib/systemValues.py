from fabric.api import *
IBM_OS = "system"

def set_system_values():
    # TO-DO more system values.
    env.shell = IBM_OS
    run('CHGSYSVAL SYSVAL(QASTLVL) VALUE(*INTERMED)')
    run('CHGSYSVAL SYSVAL(QAUTOVRT) VALUE(*NOMAX)')
    run("CHGSYSVAL SYSVAL(QCMNRCYLMT) VALUE('2 5')")
    run("CHGSYSVAL SYSVAL(QDEVRCTACB) VALUE('*ENDJOBNOLIST')")
    run("CHGSYSVAL SYSVAL(QDSCJOBITV) VALUE('60')")
    run("CHGSYSVAL SYSVAL(QJOBMSGQFL) VALUE('*WRAP')")
    #Only for non-production
    run("CHGSYSVAL SYSVAL(QLMTSECOFR) VALUE('0')")
    # IBM recomendation
    run("CHGSYSVAL SYSVAL(QPFRADJ) VALUE('3')")
    # i trust my code
    run("CHGSYSVAL SYSVAL(QVFYOBJRST) VALUE('3')")
    # time adjustment. It needs to adjust the server
     run("CHGSYSVAL SYSVAL(QTIMADJ) VALUE('QIBM_OS400_SNTP')")
 

def get_system_values():
    print("hello, getting system values")
    # To-DO for checkings