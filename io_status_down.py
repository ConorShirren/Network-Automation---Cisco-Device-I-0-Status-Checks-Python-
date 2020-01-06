#=================================================================================================
# Title:        Displaying I/O status of all interfaces that are currently DOWN on Cisco Device
# Author:       Conor Shirren
# Date:         25/11/2019
#=================================================================================================


from netmiko import ConnectHandler
from getpass import getpass
import re

print('IP address of Device you wish to SSH into:')
device_IP = input()
print('Please Enter Username:')
usr = input()

cisco_881 = {
    'device_type': 'cisco_ios',
    'host':   device_IP,            # IP Address of Device
    'username': usr,                # TACACS Username
    'password': getpass()           # ssh password of user
}

# Manually loops through each interface and checks the IO status. Very Slow but effective for Cisco IOS
net_connect = ConnectHandler(**cisco_881)
print('Enter number or switches in stack:')
switch_no = input()
for switch in range(1,switch_no+1):
    for port in range(1,49):
        output = net_connect.send_command('show int g{}/0/{} | i Last input'.format(switch,port))
        refined_output = re.search("^(.+),", output)

        if "never" in refined_output.group(1) and ":" not in refined_output.group(1):
            print('Gi{}/0/{} : '.format(switch,port) + refined_output.group(1))
        elif "w" in refined_output.group(1) and ":" not in refined_output.group(1) and "1w" not in refined_output.group(1) and "2w" not in refined_output.group(1) and "3w" not in refined_output.group(1):
            print('Gi{}/0/{} : '.format(switch,port) + refined_output.group(1))

    
