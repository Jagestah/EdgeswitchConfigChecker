#!/usr/bin/env python
#Python Ubiquiti Config Checker
#Created by JJ Mckeever - mckeeverjohnj@gmail.com
import paramiko
import time
import os
import sys
import datetime

#Gather details about the device to connect to from the Kubernetes secrets
with open('/etc/secrets/ip.txt') as device_ip:
	device_ip = device_ip.read()
with open('/etc/secrets/un.txt') as un:
	un = un.read()
with open('/etc/secrets/pwd.txt') as pw:
	pw = pw.read()

#Accept any SSH key
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#Connect to the device and get lthe running config 
ssh.connect(hostname=device_ip, username=un, password=pw)
conn = ssh.invoke_shell()
conn.send('enable\n'+pw+'\n')
conn.send('terminal length 0\n')		#Sets unlimited terminal length so the entire of the running config is sent without further input
time.sleep(1)
conn.send('show run\n')
time.sleep(1)
conn.send('no terminal length')			#Resets terminal length to the default value
run_config = conn.recv(1000000)			#Saves the running config as the variable run_config
ssh.close()

#Save a copy of the running config to a log file.
with open('/etc/logs/'+device_ip+'-backup.txt', 'w+') as backup:
	backup.write(run_config)

#Save the results of each test to a log file and add a timestamp.
logfile = open('/etc/logs/'+device_ip+'-logfile.txt', 'a+')
logfile.write(str(datetime.datetime.now())+"\r\n")

#Return the hostname of the device.
if 'snmp-server sysname' in run_config:
	split_config = run_config.split('snmp-server sysname "')
	split_config2 = split_config[1].split('"', 2)
	host_result = "The switch's hostname is:\r\n	"+split_config2[0]
	print(host_result)
	logfile.write(host_result+"\r\n")
else:
	host_result = 'Device is using default hostname'
	print(host_result)
	logfile.write(host_result+"\r\n")

#Return the number of interfaces on the switch.
int_count = str(run_config.count('interface'))
int_result = "Number of interfaces:\r\n	"+int_count
print(int_result)
logfile.write(int_result+"\r\n")

#Return the VLAN database.
if 'vlan database' in run_config:
	split_config = run_config.split('vlan database\r\nvlan ')
	split_config2 = split_config[1].split('\r\n', 2)
	vlansresult = "The following VLANs are configured on the switch:\r\n	"+split_config2[0]
	print(vlansresult)
	logfile.write(vlansresult+"\r\n")
else:
	vlansresult = 'Unable to find VLAN Database.'
	print(vlansresult)
	logfile.write(vlansresult+"\r\n")

#Return the Management VLAN.
if 'mgmt_vlan' in run_config:
	split_config = run_config.split('mgmt_vlan ')
	split_config2 = split_config[1].split('\r\n', 1)
	mgmtresult = "The management VLAN:\r\n	"+split_config2[0]
	print(mgmtresult)
	logfile.write(mgmtresult+"\r\n")
else:
	mgmtresult = 'mgmt-vlan not found'
	print(mgmtresult)
	logfile.write(mgmtresult+"\r\n")

#List number of Users
user_list = str(run_config.count('username'))
user_result = 'The switch has '+user_list+' user(s)'
logfile.write(user_result+"\r\n")
print(user_result)
for item in run_config.split("\n"):
	if "username" in item:
		item = item.split('"')
		print("	"+item[1])
		logfile.write("	"+item[1]+"\r\n")

#Count DNS name-servers and list them
dns_result = "The switch's name servers"
logfile.write(dns_result+"\r\n")
print(dns_result)
for item in run_config.split("\n"):
	if "name server" in item:
		item = item.split('ip name server ')
		print("	"+item[1])
		logfile.write("	"+item[1]+"\r\n")

#Close the logfile
logfile.close()