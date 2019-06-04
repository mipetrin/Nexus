Sample script log in and conduct a ping test. If no connectivity, perform an additional ping test. If still not responding, clear the arp cache for that particular failing IP address 

requirements:
* pip install netmiko
* ssh_device_info.py  # Used to store access credentials for devices

optional:
* cron job to execute the script every X minutes (Eg: 10 minutes) in place of continually running this script with sleep(600)


It can be executed via the following:
*  -h, --help            show this help message and exit
*  -v, --version         show program's version number and exit
*  -l, --log             Write the output to a log file: ssh_check_cmd.log.
                        Automatically adds timestamp to filename (default:
                        False)
*  -d {debug,info,warn,critical}, --debug {debug,info,warn,critical}
                        Enable debugging output to screen (default: info)


```YAML
# python ssh_check_cmd.py

# python ssh_check_cmd.py --log
```

Created by Michael Petrinovic 2019

WARNING:

These scripts are meant for educational/proof of concept purposes only - as demonstrated at Cisco Live and/or my other presentations. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and I am not responsible for any damage or data loss incurred as a result of their use
