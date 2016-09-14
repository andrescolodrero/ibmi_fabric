# ibmi_fabric
IBMi DevOps management with Fabric

Installing on windows or linux

- Python27
 Check dependencies on Fabric http://www.fabfile.org/
- pip install fabric



# To check available tasks:

 fab --list
 
# To run some tests

Edit env values (user, password and your servers name)

To test PASE COMMANDS

 fab developmentServer pase_test 
 fab -H myserver pase_test

To TEST IBMi COMMANDS:

Serial tasks

fab developmentServer tests

Parallel tasks

fab developmentServer tests2



