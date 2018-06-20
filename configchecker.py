#Python Ubiquiti Config Checker
#Created by JJ Mckeever - mckeeverjohnj@gmail.com
import paramiko
#import getpass
import time
#import re
import sys

#Gather details about the device to connect to
#device_ip = raw_input("Enter device IP: ")
#un = raw_input("Enter username: ")
#pw = getpass.getpass("Enter password: ")
#unmskey = raw_input("Enter entire UNMS Key: ")

#Arguments Passed via CLI:
#print sys.argv
device_ip = sys.argv[1]
un = sys.argv[2]
pw = sys.argv[3]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname=device_ip, username=un, password=pw)

conn = ssh.invoke_shell()
conn.send('enable\n'+pw+'\n')
conn.send('terminal length 0\n')		#Sets unlimited terminal length so the entire of the running config is sent without further input
time.sleep(1)
conn.send('show run\n')
time.sleep(1)
conn.send('no terminal length')			#Resets terminal length to the default value
run_config = conn.recv(1000000)			#Saves the running config as the variable run_config
#print(output)
ssh.close()

with open('/etc/logs/'device_ip+'-backup.txt', 'w+') as backup:
	backup.write(run_config)

#Return the number of interfaces on the switch.
int_count = str(run_config.count('interface'))
int_result = "The switch has "+int_count+" interfaces"
print(int_result)

#Return the VLAN database.
if 'vlan database' in run_config:
	split_config = run_config.split('vlan database\r\nvlan ')
	split_config2 = split_config[1].split('\r\n', 2)
	vlansresult = "The following VLANs are configured on the switch: "+split_config2[0]
	print(vlansresult)
else:
	vlansresult = 'Unable to find VLAN Database.'
	print(vlansresult)

#Return the Management VLAN.
if 'mgmt_vlan' in run_config:
	split_config = run_config.split('mgmt_vlan ')
	split_config2 = split_config[1].split('\r\n', 1)
	mgmtresult = "Management VLAN - "+split_config2[0]
	print(mgmtresult)
else:
	mgmtresult = 'mgmt-vlan not found'
	print(mgmtresult)

#Check for Voice VLAN - Currently not working
#if 'voice vlan\r\n' in run_config:
#	split_config = run_config.split('voice vlan ')
#	split_config2 = split_config[1].split('\r\n', 1)
#	print("Voice VLAN - "+split_config2[0])
#else:
#	print('Voice VLAN not found')

#List number of Users
user_list = str(run_config.count('username'))
user_result = 'The switch has '+user_list+' user(s)'
print(user_result)
for item in run_config.split("\n"):
	if "username" in item:
		item = item.split('"')
		print("	"+item[1])

#Compare unmskey against the UNMS key found in the config - not complete
#if 'unms key ' in run_config:
#	split_config = run_config.split('unms key ')
#	split_config2 = split_config[1].split('\r\n', 1)
#	mgmtresult = "Management VLAN - "+split_config2[0]
#	print(mgmtresult)
#else:
#	mgmtresult = 'mgmt-vlan not found'
#	print(mgmtresult)

#Count DNS name-servers
dns_result = "The switch's name servers"
print(dns_result)
for item in run_config.split("\n"):
	if "name server" in item:
		item = item.split('ip name server ')
		print("	"+item[1])
