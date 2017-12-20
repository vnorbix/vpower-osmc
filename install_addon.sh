#!/bin/bash

set -e

read -p 'OSMC address: ' osmc_address
read -p 'SSH username: ' osmc_user

# Copy ANT+ stick udev rules
ssh "$osmc_user@$osmc_address" << EOF
  echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0fcf", ATTRS{idProduct}=="1008", MODE="0666", RUN+="/sbin/modprobe usbserial vendor=0x0fcf product=0x1008"' | sudo tee /etc/udev/rules.d/51-ant.rules
  sudo /etc/init.d/udev restart
EOF

echo "ANT+ stick udev rules created. You can now plug in your USB ANT+ stick."

# Copy addon
scp "dist/vpower.zip" "$osmc_user@$osmc_address:/tmp/"

echo "Addon copied to /tmp. Please install the addon from your OSMC GUI".