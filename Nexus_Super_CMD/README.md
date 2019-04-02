Sample NXOS Python Script that allows you to execute a single Python script but in actual fact, it effectively executes 4 NXOS Commands. It takes the ouptut of the first command and feeds that into the second command, and then takes the output to feed into the third command, and so on.

It uses the following NXOS Commands based off the IP address specified:
* show ip arp vrf <vrf>
* show mac address-table address <mac address>
* show cdp neighbors interface <eth1/26>
* show run interface <eth 1/26>

> You need to copy these scripts over to a supported Nexus platform that is running a version of NXOS capable to execute python scripts

> Copy them over to the bootflash:scripts/ directory

Sample usage (with your appropriate IPs and VRF substituted):

Super Command = show ip arp, show mac address, show cdp, show running-config interface
```YAML
# python bootflash:scripts/nexus_supercommand_arp_mac_cdp_run.py 6.2.6.7
```

Created by Michael Petrinovic 2018

WARNING:

These scripts are meant for educational/proof of concept purposes only - as demonstrated at Cisco Live and/or my other presentations. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and I am not responsible for any damage or data loss incurred as a result of their use
