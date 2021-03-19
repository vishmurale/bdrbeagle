#!/bin/bash

port="1-1"

bind_usb(){
 echo "$1" >/sys/bus/usb/drivers/usb/bind
}

unbind_usb(){
 echo "$1" >/sys/bus/usb/drivers/usb/unbind
}

unbind_usb "$port"
sleep 1
bind_usb "$port"