#Python Ubiquiti Config Checker
#Created by JJ Mckeever - jj@greatservice.com
import paramiko
import getpass
import time
import re

#Gather details about the device to connect to
deviceIp = raw_input("Enter device IP: ")
userName = raw_input("Enter username: ")
passWord = getpass.getpass("Enter password: ")
#unmsKey = raw_input("Enter entire UNMS Key: ")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname=deviceIp, username=userName, password=passWord)

conn = ssh.invoke_shell()
conn.send('enable\n'+passWord+'\n')
conn.send('terminal length 0\n')		#Sets unlimited terminal length so the entire of the running config is sent without further input
time.sleep(1)
conn.send('show run\n')
time.sleep(1)
conn.send('no terminal length')			#Resets terminal length to the default value
runConfig = conn.recv(1000000)			#Saves the running config as the variable runConfig
#print(output)
ssh.close()

with open(deviceIp+'-backup.txt', 'w+') as backup:
	backup.write(runConfig)

#Return the number of interfaces on the switch.
intCount = str(runConfig.count('interface'))
intsresult = "The switch has "+intCount+" interfaces"
print(intsresult)

#Return the VLAN database.
if 'vlan database' in runConfig:
	splitConfig = runConfig.split('vlan database\r\nvlan ')
	splitConfig2 = splitConfig[1].split('\r\n', 2)
	vlansresult = "The following VLANs are configured on the switch: "+splitConfig2[0]
	print(vlansresult)
else:
	vlansresult = 'Unable to find VLAN Database.'
	print(vlansresult)

#Return the Management VLAN.
if 'mgmt_vlan' in runConfig:
	splitConfig = runConfig.split('mgmt_vlan ')
	splitConfig2 = splitConfig[1].split('\r\n', 1)
	mgmtresult = "Management VLAN - "+splitConfig2[0]
	print(mgmtresult)
else:
	mgmtresult = 'mgmt-vlan not found'
	print(mgmtresult)

#Check for Voice VLAN - Currently not working
#if 'voice vlan\r\n' in runConfig:
#	splitConfig = runConfig.split('voice vlan ')
#	splitConfig2 = splitConfig[1].split('\r\n', 1)
#	print("Voice VLAN - "+splitConfig2[0])
#else:
#	print('Voice VLAN not found')

#List number of Users
usersCount = str(runConfig.count('username'))
usersresult = 'The switch has '+usersCount+' user(s)'
print(usersresult)
for item in runConfig.split("\n"):
	if "username" in item:
		item = item.split('"')
		print("	"+item[1])

#Compare unmsKey against the UNMS key found in the config - not complete
#if 'unms key ' in runConfig:
#	splitConfig = runConfig.split('unms key ')
#	splitConfig2 = splitConfig[1].split('\r\n', 1)
#	mgmtresult = "Management VLAN - "+splitConfig2[0]
#	print(mgmtresult)
#else:
#	mgmtresult = 'mgmt-vlan not found'
#	print(mgmtresult)

#Count DNS name-servers
dnsresult = "The switch's name servers"
print(dnsresult)
for item in runConfig.split("\n"):
	if "name server" in item:
		item = item.split('ip name server ')
		print("	"+item[1])