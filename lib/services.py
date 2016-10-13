from fabric.api import *
IBM_OS = "system"
DNS1= ""
DNS2=""

def set_services():
    env.shell = IBM_OS
    # Configure NTP servers
    command = "chgntpa RMTSYS('" + DNS1 +"' '" + DNS2 + "') AUTOSTART(*YES)"
    run(command)
    # Apache Config - Reverse Proxy
    