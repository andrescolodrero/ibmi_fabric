from fabric.api import *
from fabric.colors import *
IBM_PASE = "/QOpenSys/usr/bin/bsh -c"
IBM_OS = "system"
#env.user = "acl"
#env.key_filename = 'id_rsa.pub'

env.roledefs = {                                                              
    'source': ['disibic22'],                                           
    'target': ['tisibic22','disibic21','tisibic21','aisibic21','aisibic22'],                                 
}

 
 
    #print(command_savf)
    #run("CRTSAVF FILE(QTEMP/' + library  + ')")
    #run('SAVLIB LIB('" + LIBRARY + '"') DEV(" + SAVF + ")') 

def get_file(library):
    env.shell = IBM_OS
    # remove the Local File
    with settings(warn_only=True):
        local("rm /mnt/c/pythonmanagement/SAVF.FILE")
    # Create savf.
    # I got always CPA4067 error from SSH session even with the RPLLE entry
    run("CRTSAVF FILE(FABRIC/FABRIC)")
    command_savlib = "SAVLIB LIB(" + library + ") DEV(*SAVF) SAVF(FABRIC/FABRIC)"
    run(command_savlib)
    # put files on my local computer or server fabric
    get('/QSYS.LIB/FABRIC.LIB/FABRIC.FILE','/mnt/c/pythonmanagement/SAVF.FILE')
    # removing the file
    run("DLTOBJ OBJ(FABRIC/FABRIC) OBJTYPE(*FILE)")


def put_file(library):
    env.shell = IBM_OS
    with settings(warn_only=True):
        result = put('/mnt/c/pythonmanagement/SAVF.FILE','/QSYS.LIB/FABRIC.LIB/SAVF.FILE')
    if result.failed:
        print(red("Deployment of library " + library + " failed"))
    else:
        command = "RSTLIB SAVLIB(" + library +") DEV(*SAVF)  SAVF(FABRIC/SAVF)"
        run(command) 
        print(yellow("Deployment of library " + library + " succeeded"))

       
        
    

def deploy_savf(library):
    env.shell = IBM_OS
    #Get Files from source
    get_file.roles = ('source',)   
    execute(get_file, library)
    # Put files on target
    put_file.roles = ('target',)
    execute(put_file,library)

@roles('source','target')
def initsavfile():
    env.shell = IBM_OS
    # Create library
    with settings(warn_only=True):
        result = run("CRTLIB FABRIC")
    
    with settings(warn_only=True):
        run("CRTSAVF FILE(FABRIC/SAVF)")
    # change Reply List entry for the FILE
    with settings(warn_only=True):
        result = run("ADDRPYLE SEQNBR(800) MSGID(CPA4067) CMPDTA(FABRIC 2) RPY(G)")
    if result.failed: 
        run("CHGRPYLE SEQNBR(800) MSGID(CPA4067) CMPDTA(FABRIC 2) RPY(G)")

