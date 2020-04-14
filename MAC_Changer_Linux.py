#!/usr/bin/env python3

import subprocess
import os
import random
import re
import optparse


def choose_interface(interface):
    interface = int(input("Chose out of the {} only one:".format(len(interfaces))))
    while interface not in range(1, len(interfaces)+1):
        interface = int(input("Error, chose out of the {} only one:".format(len(interfaces))))
    return interface


def available_nic(interfaces):
    print("the available NIC interfaces are:")
    for i in range(len(interfaces)):
        print("{}: {}".format(i + 1, interfaces[i]))


def anser_randmoize():
    answer = input("Do you want randomized MAC address? (yY/nN) ")
    while answer not in ["y", "Y", "n", "N"]:
        answer = input("Incorrect, do you want randomized MAC address? (you can only choose y/Y or n/N) ")
    return answer


def mac_validator():
    new_mac = input("Please enter the new MAC address (aa:bb:cc:dd:ee:ff) [0-9][A-F]: ")
    while not re.match("[0-9a-f]{2}(:?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", new_mac.lower()):
        new_mac = input("Error, please enter the new MAC address (aa:bb:cc:dd:ee:ff) [0-9][A-F]: ")
    return new_mac


interfaces = os.listdir('/sys/class/net/')
parser = optparse.OptionParser()

parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
parser.parse_args()
subprocess.call(["sudo", "ifconfig"])

available_nic(interfaces)

interface = choose_interface(interfaces)-1
print("Change MAC address for {}".format(interfaces[interface]))

subprocess.call(["sudo", "ifconfig", interfaces[interface], "down"])

answer = anser_randmoize()

if answer in ["y", "Y"]:
    new_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
else:
    new_mac = mac_validator()

subprocess.call(["sudo", "ifconfig", interfaces[interface], "hw", "ether", new_mac])
subprocess.call(["sudo", "ifconfig", interfaces[interface], "up"])
subprocess.call(["sudo", "ifconfig", interfaces[interface]])
