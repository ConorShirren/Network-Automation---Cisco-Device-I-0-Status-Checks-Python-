#=================================================================================================
# Title:        Displaying I/O status of all interfaces that are currently UP on Cisco Device
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
    'host':  device_IP,            # IP Address of Device
    'username': usr,               # TACACS Username
    'password': getpass()          # ssh password of user
}

net_connect = ConnectHandler(**cisco_881)
output = net_connect.send_command('show ip int brief | i up')
up_ints_file = open("up_ints_file.txt", "w")
n = up_ints_file.write(output)
up_ints_file.close()
lines = open('up_ints_file.txt','r').readlines()
ints = []
print('\n\n\n')
print(lines)
for a in lines:
    refined_output = re.search("^[^\s]+", a)
    ints.append(refined_output.group())
int_io_status = open("int_io_status.txt", "w")
for interface in ints:
    output = net_connect.send_command('show int {} | i Last input'.format(interface))
    refined_output = re.search("^(.+),", output)
    x = '{} : '.format(interface) + refined_output.group(1)
    n = int_io_status.write(x + '\n')
    print(x)
  
int_io_status.close()  


