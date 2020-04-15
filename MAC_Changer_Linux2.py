#!/usr/bin/env python3

import subprocess
import re
import optparse


def mac_validator(new_mac):
    while not re.match("[0-9a-f]{2}(:?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", new_mac.lower()):
        new_mac = input("Error, please enter the new MAC address (aa:bb:cc:dd:ee:ff) [0-9][A-F]: ")
    return new_mac



def change_mac(interface, new_mac):
    print("[+] Change MAC address for {} to {}".format(interface, new_mac))
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])
    print("[+] MAC address changed successfully to " + new_mac)


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help/-h for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC or random, use --help/-h for more info.")
    elif str(options.new_mac) == "None":
        parser.error("[-] Please specify a new MAC, use --help/-h for more info.")
    return options


def current_mac(interface):
    original_mac = subprocess.check_output(["sudo", "-S", "ifconfig", interface])
    current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", original_mac.decode("ascii"))
    if current_mac:
        return current_mac.group(0)
    else:
        print("[-] Couldn't read the MAC address")


options = get_arguments()
current_mac = current_mac(options.interface)
print("Current MAC address: " + current_mac)

if current_mac == options.new_mac:
    print("[+] The MAC that you have entered is the same")
    exit(1)
elif options.new_mac:
    current_mac = mac_validator(options.new_mac)
else:
    print("Error changing MAC")

change_mac(options.interface, str(current_mac))
