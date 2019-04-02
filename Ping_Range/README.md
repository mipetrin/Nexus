Sample NXOS Python Script that allows you to specify a Subnet Range and VRF in order to perform a Ping Sweep and see the results. It performs 2 complete sweeps in the event that the script misses the ping response during the first sweep or it takes time for ARP to resolve.

> You need to copy these scripts over to a supported Nexus platform that is running a version of NXOS capable to execute python scripts

> Copy them over to the bootflash:scripts/ directory

Sample usage (with your appropriate IPs and VRF substituted):

Ping Range:
```YAML
# python bootflash:scripts/ping_range.py 6.2.6.3-7 vrf mipetrin-CLUS18
```

Created by Michael Petrinovic 2018

WARNING:

These scripts are meant for educational/proof of concept purposes only - as demonstrated at Cisco Live and/or my other presentations. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and I am not responsible for any damage or data loss incurred as a result of their use
