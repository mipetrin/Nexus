#! /usr/bin/env python
"""
Script to log in and conduct a ping test. If no connectivity, perform an additional ping test. If still not responding, clear the arp cache for that particular failing IP address

Requirements:
    cron job to execute the script every X minutes (Eg: 10 minutes) in place of continually running this script with sleep(600)?

"""

__version__ = 0.1

##############
# Imports
##############

import re
import os
import time
import logging
import sys

try:
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
except ImportError:
    print "Error: Need to install the argparse module: 'pip install argparse'"
    exit(0)

try:
    from netmiko import ConnectHandler
except ImportError:
    print "Error: Need to install the netmiko module: 'pip install netmiko'"
    exit(0)

try:
    # Import configuration from another python file for simplicity.
    from ssh_device_info import nexus as device
except ImportError:
    print "Error: Need to also have the ssh_device_info.py in the same directory as this script. Ensure it is available and readable" # If have multiple, need to think ahead
    exit(0)


##############
# Globals
##############

# Create a custom logger
logger = logging.getLogger(__name__)
logger.propagate = False # Required to prevent the same logging message appearing twice
logging_filename = "" # Filename to be used if --log option used. Set during setup_logger()


##############
# My Functions
##############

def setup_logger(logger, level, write_file):
    '''
    Set up my custom Logger
    '''
    # Create handlers
    logging_level = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARNING,
        "critical": logging.CRITICAL,
    }.get(level, logging.DEBUG) # Although fallback is debug, actually argparse option sets default to info

    # Set logging level as specified on the command line via --debug
    logger.setLevel(logging_level)

    # Logger Formatting
    plain_formatter = "" # Basic Format to make use of Logger functionality but present it as normal "print" output on the console
    file_formatter = "%(asctime)s.%(msecs).03d || %(levelname)8s || "
    file_formatter += "(%(lineno)4d) || %(message)s"
    date_formatter = "%Z %Y-%m-%dT%H:%M:%S"

    # Console Logger
    logger_stdout_handler = logging.StreamHandler(sys.stdout)
    logger_stdout_handler.setFormatter(logging.Formatter(
        fmt=plain_formatter,
        datefmt=date_formatter)
    )
    logger.addHandler(logger_stdout_handler)

    # Check if --log specified on CLI to write logging output to a log file as well
    if write_file:
        full_script_name = os.path.basename(__file__)
        my_script_split = full_script_name.split(".py")
        script_name = my_script_split[0]

        # Get Time to save in the .log file.
        time_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%d_%m_%Y_%H_%M_%S", time_tuple)

        # Setup filename for log file output. Eg: compare_ep_move_08_04_2019_22_24_22.log
        script_name_ext = "{}_{}.log".format(script_name, time_string)
        global logging_filename
        logging_filename = script_name_ext

        # Create File Handler
        logger_file_handler = logging.FileHandler(script_name_ext, mode='w') # Default option is mode='a' / append. =w overwrites
        logger_file_handler.setLevel(logging_level)

        # Create File Formatter and add it to handlers
        logger_file_handler.setFormatter(logging.Formatter(
            fmt=file_formatter,
            datefmt=date_formatter)
        )

        # Add handlers to the logger
        logger.addHandler(logger_file_handler)
        logger.info("Log file being written: {}\n".format(script_name_ext))
    else:
        logger.info("Log file NOT being written\n")


def get_parser():
    '''
    Get parser object for script
    '''
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter,
                            add_help=True,
                            version=__version__)
    parser.add_argument("-l", "--log", action='store_true', help='Write the output to a log file: {}.log. Automatically adds timestamp to filename'.format(__file__.split(".py")[0]))
    parser.add_argument("-d", "--debug", dest="debug", choices=["debug", "info", "warn", "critical"], default="info", help='Enable debugging output to screen')
    return parser


def make_connection (ip,username,password):
    try:
        return ConnectHandler(ip = device["address"],
                            port = device["ssh_port"],
                            username = device["username"],
                            password = device["password"],
                            device_type = device["device_type"])
    except Exception as e:
        logger.info("ERROR has occurred: {}".format(e))
        return False


def print_error(msg):
    logger.info("Exception Caught: {}".format(msg))


def main():
    '''
    Main Function and core logic of the script
    '''
    # Get the CLI arguements
    args = get_parser().parse_args()

    # Set up custom logger
    setup_logger(logger, args.debug, args.log)

    total_start = time.time()

    # Create a CLI command template
    cmd_ping_map = "ping {} count {} vrf {}"
    cmd_clear_arp_map = "clear ip arp {}"

    ip_addresses_to_check = {
        "N3K":"6.2.6.3",
        "N5K":"6.2.6.5",
        "N7K":"6.2.6.7"
    }

    for hostname, ip_addr in ip_addresses_to_check.iteritems():
        logger.debug("Hostname '{}' has IP Address '{}'".format(hostname, ip_addr))

        # Open CLI connection to device
        try:
            my_connection = make_connection("ip","user","pass") # Device to check from and clear if necessary

            logger.info("Performing 1st attempt to {} / {} with 1 ping".format(hostname, ip_addr))
            command = cmd_ping_map.format(ip_addr, "1", "default")
            output = my_connection.send_command(command)

            # Print the raw command output to the screen
            logger.debug("1" * 30)
            logger.debug("Raw CLI Output:\n" + output)
            logger.debug("1" * 30)

            try:
                # Use regular expressions to parse the output for desired data
                summary = re.search(r' 0.00% packet loss', output) # Notice it is ' 0.00%' and not '0.00%' so as to not also capture 100.00 vs 0.00

                if summary:
                    # Found a match, skip
                    logger.debug("Found match: '{}'".format(summary.group()))
                    logger.info("Ping was succesful on 1st attempt")
                    pass
                else:
                    # Not 0.00% packet loss, therefore not responding
                    # perform a 2nd iteration of ping, with 3 repeat
                    logger.info("Failed 1st attempt")
                    logger.info("Performing 2nd attempt with 3 pings")
                    command = cmd_ping_map.format("6.2.6.7", "3", "default")
                    output = my_connection.send_command(command)
                    logger.debug("2" * 30)
                    logger.debug("Raw CLI Output:\n" + output)
                    logger.debug("2" * 30)

                    try:
                        # Use regular expressions to parse the output for desired data
                        summary = re.search(r' 0.00% packet loss', output) # Notice it is ' 0.00%' and not '0.00%' so as to not also capture 100.00 vs 0.00
                        if summary:
                            # Found a match, skip
                            logger.info("Ping was succesful on 2nd attempt")
                            pass
                        else:
                            # Not 0.00% packet loss, therefore not responding
                            # Now need to clear the arp entry
                            logger.info("Failed 2nd attempt")
                            logger.info("Performing a clear of the ARP Cache")
                            command = cmd_clear_arp_map.format("6.2.6.7")
                            output = my_connection.send_command(command)
                            logger.debug("3" * 30)
                            logger.debug("Raw CLI Output:\n" + output)
                            logger.debug("3" * 30)
                            logger.info("Completed clearing the ARP cache for {}/{}".format(hostname, ip_addr))
                    except Exception as e:
                        logger.critical("\nCannot find ' 0.00%' in ouptut. Need to debug")
                        print_error(e)
            except Exception as e:
                logger.critical("\nCannot find ' 0.00%' in ouptut. Need to debug")
                print_error(e)
        except Exception as e:
            print_error(e)

        logger.info("#" * 30)

    if args.log:
        logger.info("\nLog file written: {}\n".format(logging_filename))

    total_end = time.time()
    logger.info("\nEnd of Script -- Total Execution Time: {}".format(total_end - total_start))


if __name__ == '__main__':
    main()
