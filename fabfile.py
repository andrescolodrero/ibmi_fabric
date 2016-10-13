from fabric.api import *
from fabric.contrib.console import confirm
from fabric.colors import *
import logging
import lib.services as services
import lib.systemValues as systemValues
import lib.securitySettings as securitySettings
import lib.fileTransfer as fileTransfer

IBM_PASE = "/QOpenSys/usr/bin/bsh -c"
IBM_OS = "system"
<<<<<<< HEAD
env.user = "ACL"
env.key_filename = 'id_rsa.pub'

=======
env.user = ""
env.password = ""
>>>>>>> origin/master

# define logging

logging.basicConfig(
    filename="deploy.log",
    level=logging.WARNING  
)

env.roledefs = {                                                              
    'dev': ['disibic22'],                                           
    'test': ['tisibic22'],                                 
}

def all_servers():
    env.hosts = ['disibic21', 'disibic22',
    'tisibic21', 'tisibic22',
    'aisibic21', 'aisibic22']

def developmentServers():
# Define my hosts.
     env.hosts = ['disibic21', 'disibic22']
def testServers():
# Define my hosts.
     env.hosts = ['tisibic21', 'tisibic22']
     
def productionServers():
# Define my hosts.
     env.hosts = ['aisibic21', 'aisibic22']

def pase_test(): 
    env.shell = IBM_PASE
    run('uname -s')


def init_setup():
    env.shell = IBM_PASE
    run("uname -s")
    # Do check, dont espape warning errors
    # i expect the file will not exists
    with settings(warn_only=True):
    # home is not setup by default after CRTUSRPRF
        result = run('bsh -f /home/' + env.user)
        logging.warning(" Home directory not setup for " + env.user )
    if result.failed: 
        print("Directory doesnt exist. Creating /home/" + env.user)
        run("mkdir /home/" + env.user)

@parallel
def tests():
    env.shell = IBM_OS
    print(green("Starting Deployment"))
    run("dspmsg qsysopr")
    run("DSPSYSVAL SYSVAL(QPWDEXPITV)")

def get_library():
    print("Create SAV File")
    get('/QSYS.LIB/ACL.LIB/USERS.FILE','/mnt/c/pythonmanagement/USERS.FILE')

def put_file():
    put('/mnt/c/pythonmanagement/USERS.FILE/USERS.FILE','/QSYS.LIB/ACL.LIB/')

def deploy_file(source_role, target_role):
    env.shell = IBM_OS
    get_file.roles = (source_role,)                                       
    execute(get_file)

    put_file.roles = (target_role,)                                       
    execute(put_file)

@parallel
def deploy_ibmi():
    print(green("Starting Deployment"))
    env.shell = IBM_OS
    print(green("Setting Security Values"))
    execute(securitySettings.set_security_values)
    execute(securitySettings.syslog_setup)
    execute(securitySettings.turn_off_default_servers)
    print(yellow("........................................."))
    print(green("Setting System Values"))
    execute(systemValues.set_system_values)
    # change SHELL
    env.shell = IBM_PASE
    execute(services.set_services)
    #execute(nodeJSSetup.set_global_packages)
    print(green("Deployment finish"))

   
# TODO:
# Set Enviromental Variables
# Check values

