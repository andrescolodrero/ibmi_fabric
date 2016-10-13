
from fabric.api import *
import os
from fabric.colors import *

IBM_OS = "system"
IBM_PASE = "/QOpenSys/usr/bin/bsh -c"
# i insert user and key here for testing
#env.user = "acl"
#env.key_filename = 'id_rsa.pub'

def set_security_values():
    env.shell = IBM_OS
    run("CHGSYSVAL SYSVAL(QPWDEXPITV) VALUE('90')")
    run("CHGSYSVAL SYSVAL(QPWDLMTREP) VALUE('2')")
    # bASIC AND OLD SEC SETTINGS. NON-SECURE
    run("CHGSYSVAL SYSVAL(QPWDMAXLEN) VALUE(10)")
    run("CHGSYSVAL SYSVAL(QPWDMINLEN) VALUE(5)")
    run("CHGSYSVAL SYSVAL(QPWDRQDDIF) VALUE('7')")
    # Necesary for PowerHA
    run("CHGSYSVAL SYSVAL(QRETSVRSEC) VALUE('1')")
    # and the most important
    run("CHGSYSVAL SYSVAL(QSECURITY) VALUE('30')")
    #run("CHGSYSVAL SYSVAL(QSECURITY) VALUE('40')")
    # more jobqentryes in qbatch
    run('CHGJOBQE SBSD(QSYS/QBATCH) JOBQ(QGPL/QBATCH) MAXACT(*NOMAX)')

  
def turn_off_default_servers():
    env.shell = IBM_OS
    # By default some servers are ON on IBMI, lets stop unnecesary servers
    run("ENDTCPSVR SERVER(*LPD)")
    # END LDAP
    run("ENDTCPSVR SERVER(*DIRSRV)")
    run("ENDTCPSVR SERVER(*SMTP)")
    run("ENDTCPSVR SERVER(*OMPROUTED)")


def get_system_values():
    print("test")
    # To-DO for checkings

def syslog_setup():
    env.shell = IBM_PASE
    # create log file for syslog_setup
    with settings(warn_only=True):
        run('mkdir /var/log')
    
    run("touch /var/log/messages")
    run("touch /var/log/auth")
    # Put syslog Config
    put(os.getcwd() + '/config/syslog.conf','/QOpenSys/etc/syslog.conf')
    put(os.getcwd() + '/config/motd','/etc/motd')
    # is syslogd running already?
    env.shell = IBM_OS
    with settings(warn_only=True):
       result = run("wrkactjob | grep 'syslogd'")
    if result.failed:
        # start syslog
        print("Starting syslogd")
        run("SBMJOB CMD(STRQSH CMD('/QOpenSys/usr/sbin/syslogd'))")
    else:
        JobName = result[0:9]
        UserName = result[13:23]
        JobNumber = result[25:31]
        print(JobName + '/' + UserName + '/' + JobNumber)

        command = "ENDJOB JOB(" + JobNumber.strip() + "/" + UserName.strip() + "/" + JobName.strip() + ") OPTION(*IMMED)"
        run(command)
        run("SBMJOB CMD(STRQSH CMD('/QOpenSys/usr/sbin/syslogd'))")

def ssh_setup():
    env.shell = IBM_PASE
    #STop SSH Daemon
    run("system 'endtcpsvr server(*SSHD)'")
    # Generate Public and Private keys
    run('ssh-keygen -t rsa1 -f /QOpenSys/QIBM/UserData/SC1/OpenSSH/etc/ssh_host_key -N ""')
    run('ssh-keygen -t dsa -f /QOpenSys/QIBM/UserData/SC1/OpenSSH/etc/ssh_host_dsa_key -N ""')
    run('ssh-keygen -t rsa -f /QOpenSys/QIBM/UserData/SC1/OpenSSH/etc/ssh_host_rsa_key -N ""')
    run("system 'ENDSBS SBSOSS'")
    run("system 'STRSBS OSSLIB/SBSOSS'")
    #put(os.getcwd() + '/config/syslog.conf','/QOpenSys/etc/syslog.conf')
        
def subsystem_oss():
    env.shell = IBM_OS
    # Check if Library Exists
    with settings(warn_only=True):
        result = run("CRTLIB OSSLIB")
    if result.failed:
        print(yellow("Setup has been completed"))
    else:
        # Create an OSS Subsystem for SSH, SCP, etc.
        run("CRTSBSD SBSD(OSSLIB/SBSOSS) POOLS((1 *BASE)) TEXT('OSS jobs subsystem')")
        run("CRTJOBQ JOBQ(OSSLIB/OSSJOBQ) TEXT('OSS job queue')")
        with settings(warn_only=True):
            run("CRTUSRPRF USRPRF(OSSDUSR) PASSWORD(*NONE) INLMNU(*SIGNOFF) LMTCPB(*YES) SPCAUT(*ALLOBJ)  TEXT('OSS Daemon user profile')")
        #ssh autostart
        run("CRTJOBD JOBD(OSSLIB/SSHJOBD) JOBQ(OSSLIB/OSSJOBQ) TEXT('Job description for SSHD autostart')  USER(OSSDUSR) RQSDTA('CALL PGM(QP2SHELL) PARM(''/QOpenSys/usr/sbin/sshd'')')")
        # Configure Syslog Autostart on this subsystem_oss
        run("CRTJOBD JOBD(OSSLIB/SYSLJOBD) JOBQ(OSSLIB/OSSJOBQ) TEXT('Job description for SSHD autostart')  USER(OSSDUSR) RQSDTA('CALL PGM(QP2SHELL) PARM(''/QOpenSys/usr/sbin/syslogd'')')")
        #
        run("CRTCLS CLS(OSSLIB/OSSCLS) TEXT('OSS job class')")
        run("ADDRTGE SBSD(OSSLIB/SBSOSS) SEQNBR(1) CMPVAL(*ANY) PGM(QCMD) CLS(OSSLIB/OSSCLS)")
        run("ADDJOBQE SBSD(OSSLIB/SBSOSS) JOBQ(OSSLIB/OSSJOBQ) MAXACT(*NOMAX) SEQNBR(10)")
        run("ADDJOBQE SBSD(OSSLIB/SBSOSS) JOBQ(OSSLIB/OSSJOBQ) MAXACT(*NOMAX) SEQNBR(10)")
        run("ADDAJE SBSD(OSSLIB/SBSOSS) JOB(SSHD) JOBD(OSSLIB/SSHJOBD)")
        run("ADDAJE SBSD(OSSLIB/SBSOSS) JOB(SYSLOG) JOBD(OSSLIB/SYSLJOBD)")
        print(green(" Setup Complete. Please STOP SSHD with ENDTCPSVR *SSHD and start OSSSBS Subsystem"))
        print(green("You could have a msg like sshd[21954]: fatal: Cannot bind any address. "))
        #run("system 'ENDSBS SBSOSS'")
        #run("system 'STRSBS OSSLIB/SBSOSS'")




