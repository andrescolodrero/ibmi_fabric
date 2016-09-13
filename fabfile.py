from fabric.api import *
import logging


IBM_PASE = "/QOpenSys/usr/bin/bsh -c"
IBM_OS = "system"
env.user = "ACL"

# define logging

logging.basicConfig(
    filename="deploy.log",
    level=logging.WARNING  
)

def all_servers():
    env.hosts = ['disibic21', 'disibic22',
    'tisibic21', 'tisibic22',
    'aisibic21', 'aisibic22']

def development():
# Define my hosts.
     env.hosts = ['disibic21', 'disibic22']
def test():
# Define my hosts.
     env.hosts = ['tisibic21', 'tisibic22']
     
def production():
# Define my hosts.
     env.hosts = ['aisibic21', 'aisibic22']

def pase_test(): 
    env.shell = IBM_PASE
    run('uname -s')

def system_values():
    env.shell = IBM_OS
    run('dspsysval qautovrt')

def init_setup():
    env.shell = IBM_PASE
    
    # Do check, dont espape warning errors
    # i expect the file will not exists
    with settings(warn_only=True):
    # home is not setup by default after CRTUSRPRF
        result = run('bsh -f /home/' + env.user)
        logging.warning(" Home directory not setup for " + env.user )
    if result.failed: 
        print("Directory doesnt exist. Creating /home/" + env.user)
        run("mkdir /home/" + env.user)

def system_values():
    # TO-DO more system values.
    env.shell = IBM_OS
    run('CHGSYSVAL SYSVAL(QASTLVL) VALUE(*INTERMED)')

def security_auditing():
    env.shell = IBM_OS
    run('CHGSECAUD QAUDCTL(*ALL) QAUDLVL(*DFTSET)')

def deploy():
    execute(pase_test)
    execute(system_values)
    execute(security_auditing)
   
# TODO:
# Set Enviromental Variables
# Check values

