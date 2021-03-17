#!/usr/bin/env python3
import pyshark
import netifaces as ni
import argparse
import os
import sys

INTERFACES = os.listdir("/sys/class/net")

parser = argparse.ArgumentParser(description="Flashes camera LEDs on network activity")

parser.add_argument("--interface", help="The network interface to monitor", required=True, choices=INTERFACES)

args = parser.parse_args()

if not os.geteuid() == 0:
  sys.exit("\nOnly root can run this script\n")

capture = pyshark.LiveCapture(interface=args.interface)
interfaces = ni.ifaddresses(args.interface)

myip = "" # your ip

camera = "" # where your video camera is, mine was /dev/video0

capture = pyshark.LiveCapture(interface=args.interface)

for i in interfaces.values():

  if "192.168" in i[0]["addr"]:
    myip = i[0]["addr"]
    break

print(f"ip {myip}")

try:
  for packet in capture.sniff_continuously():
      if "ip" in packet:
          if packet.ip.dst == myip:
              os.system(f'timeout 0.1 mpv --no-video --no-audio {camera} >/dev/null 2>&1')
except KeyboardInterrupt:
  pass

