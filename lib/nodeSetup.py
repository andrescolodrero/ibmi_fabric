from fabric.api import *
IBM_PASE = "/QOpenSys/usr/bin/bsh -c"

DNS1= "10.32.96.12"
DNS2="10.23.64.12"

def set_global_packages():
    env.shell = IBM_PASE
    # Configure NTP servers
    run("npm install -g grunt gulp supervisor")
    run(command)