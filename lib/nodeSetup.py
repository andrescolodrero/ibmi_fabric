from fabric.api import *
IBM_PASE = "/QOpenSys/usr/bin/bsh -c"
#env.user = "acl"
#env.key_filename = 'id_rsa.pub'
def set_global_packages():
    env.shell = IBM_PASE
    # Setup Node4 as basic Node4
    run('ln -s /usr/bin/node /QOpenSys/QIBM')
    #todo -> PATH.. not taking .profile ?
    #run("npm install -g grunt gulp supervisor")
    run("env")