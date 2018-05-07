Created by Michael Petrinovic 2018

Sample Nexus On-Board Python Scripts for:
* Cisco Live Melbourne 2018: BRKDCN-2602
* Cisco Live USA 2018: BRKDCN-2011

You need to copy these scripts over to a supported Nexus platform that is running a version of NXOS capable to execute python scripts

Copy them over to the bootflash:scripts/ directory

Sample usage (with your appropriate IPs and VRF substituted):

Ping Range:
```YAML
# python bootflash:scripts/ping_range.py 6.2.6.3-7 vrf mipetrin-CLUS18
```

Super Command = show ip arp, show mac address, show cdp, show running-config interface
```YAML
# python bootflash:scripts/nexus_supercommand_arp_mac_cdp_run.py 6.2.6.7
```
