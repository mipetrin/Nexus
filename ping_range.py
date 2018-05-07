#!/usr/bin/env python
'''
This script is a simple 'supercommand', where a sequence of four common commands,
show ip arp, show mac address-table, show cdp neighbor, show run interface
are all chained with their outputs fed into each other to gather information
about a particular device connected to this switch.

Original code:
https://github.com/datacenter/who-moved-my-cli/blob/master/pingrange.py

Very little modification. Changed some of the formatting of the output as well as
hard coding some of the options (ie. count 1) to make easier to demo

Michael Petrinovic 2018
'''

import re
try:
        from cli import cli
except ImportError:
        from cisco import cli
from argparse import ArgumentParser

def expandrange(rangefunc):
    hosts = []
    octets = rangefunc.split('.')
    for i,octet in enumerate(octets):
        if '-' in octet:
            octetrange = octet.split('-')
            for digit in range(int(octetrange[0]), int(octetrange[1])+1):
                ip = '.'.join(octets[:i] + [str(digit)] + octets[i+1:])
                hosts += expandrange(ip)
            break
    else:
        hosts.append(rangefunc)
    return hosts

parser = ArgumentParser('pingrange')
parser.add_argument('ip', help='IP range to ping, e.g., 10.1.0-1.0-255 will expand to 10.1.0.0/23')
parser.add_argument('options', nargs='*', help='Options to pass to ping', default=['count 1'])
args = parser.parse_args()
targets = expandrange(args.ip)

for ip in targets:
    m = re.search('([0-9\.]+)% packet loss', cli('ping %s count 1 %s' % (ip, ' '.join(args.options))))
    print('%s - %s' % (ip, 'UP' if float(m.group(1)) == 0.0 else 'DOWN'))

print "Performing second sweep to double check...\n"

for ip in targets:
    m = re.search('([0-9\.]+)% packet loss', cli('ping %s count 1 %s' % (ip, ' '.join(args.options))))
    print('%s - %s' % (ip, 'UP' if float(m.group(1)) == 0.0 else 'DOWN'))
