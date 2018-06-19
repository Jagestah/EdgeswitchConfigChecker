# EdgeswitchConfigChecker
Use a Python script to check pertinent details of a Ubiquiti Edgeswitch's configuration

#-------------------Operational Description-------------------
This script prompts for a device IP address, username, and password.  
Then it uses the supplied info to SSH to the device, get in to `enable` mode and then run the command `show run`  
A backup file named `<deviceIP>-backup.txt` is created in the same folder as the script.  
The script then checks the running config for pertinent details:  
  * Number of interfaces  
  * VLANs in VLAN Database  
  * The Management VLAN  
  * The number of users as their names  
  * The switch's Name Server(s)  