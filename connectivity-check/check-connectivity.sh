#!/bin/bash

count=$(ip link show up | grep 'link/' | grep -v 'link/loopback' | wc -l)

if [ $count -lt 1 ]
then
  echo "Netwroking down"
  exit 1
else
  echo "Networking up"
  exit 0
fi