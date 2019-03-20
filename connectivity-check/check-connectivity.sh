#!/bin/bash

# check for at least one 'up' network interface
# to run on startup, invoke from /etc/rc.local, create an inittab, or a @reboot cronjob

count=$(ip link show up | grep 'link/' | grep -v 'link/loopback' | wc -l)

if [ $count -lt 1 ]
then
  echo "Netwroking down"
  exit 1
else
  echo "Networking up"
  exit 0
fi