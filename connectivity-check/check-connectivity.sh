#!/bin/bash

#ref: https://stackoverflow.com/a/6119327/577298
#ref: https://stackoverflow.com/a/26392064/577298
ping -w 30 -c 5 8.8.8.8 > /dev/null && echo "up" || echo "down"
