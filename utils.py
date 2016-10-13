from fabric.api import *
from fabric.contrib.console import confirm
from fabric.colors import *
import logging
import lib.services as services
import lib.systemValues as systemValues
import lib.securitySettings as securitySettings
import lib.nodeSetup as nodeJSSetup

IBM_PASE = "/QOpenSys/usr/bin/bsh -c"
IBM_OS = "system"
env.user = "ACL"
env.key_filename = 'id_rsa.pub'

# define logging

logging.basicConfig(
    filename="deploy.log",
    level=logging.WARNING  
)

./chroot_setup.sh chroot_libs.lst /QOpenSys/andres
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

def create_savf(library):
     env.hosts = ['disibic22']
    env.shell = IBM_OS
    run('SAV ACL')

def get_file():
    print("hola")
    SAVF
    get SAV
    get('/QSYS.LIB/ACL.LIB/USERS.FILE','/mnt/c/pythonmanagement/USERS.FILE')

def put_file():
    put('/mnt/c/pythonmanagement/USERS.FILE/USERS.FILE','/QSYS.LIB/ACL.LIB/')

    RSTSAVF

def deploy_file(source_role, target_role):
    env.shell = IBM_OS
    get_file.roles = (source_role,)                                       
    execute(get_file)

    put_file.roles = (target_role,)                                       
    execute(put_file)



