from fabric.api import *
IBM_OS = "system"
DNS1= "10.32.96.12"
DNS2="10.23.64.12"

def set_services():
    env.shell = IBM_OS
    # Configure NTP servers
    command = "chgntpa RMTSYS('" + DNS1 + DNS2 + "') AUTOSTART(*YES)"
    #run(command)
    print("hello " + command)