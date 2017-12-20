# Virtual power Raspberry PI OSMC service

This service can emit virtual power data to ANT+ bike head units and computers based on [bike trainers](https://en.wikipedia.org/wiki/Bicycle_trainer) power curve. It utilizes speed data from [ANT+](https://en.wikipedia.org/wiki/ANT%2B) sensors. With an ANT+ stick plugged in to Raspberry PI (running OSMC) and installing an addon, you can receive virtual power data on your bike head unit/computer. This OSMC addon is based on [vpower](https://github.com/dhague/vpower) application.

## Prerequisites

With the below you can install the service on OSMC.

* Raspberry PI with [OSMC](https://osmc.tv/)
* bike trainer (at the moment supported bike trainers are KurtKinetic, BT-ATS, Tacx Blue Motion)
* ANT+ stick (Suunto, Garmin - though only older models are working)
* ANT+ speed (or candence+speed) sensor (e. g. Garmin)
* ANT+ head unit / bike computer

## Install addon

1. Enable SSH server in your OSMC at My OSMC -> Services -> SSH Server, if it's not yet enabled. Default username/password is osmc/osmc.
2. Run install acript: `./install_addon.sh`, follow the instuctions. This will create a udev rule to allow to service to access the ANT+ stick, then copy the addon zip file from /dist to /tmp.
3. Plug in your ANT+ stick into your PI.
4. Install the addon in OSMC. Choose install from zip file then browse to /tmp/vpower.zip in your root filesystem.
5. Service is automatically started, otherwise it can be started and stopped in My addons -> services.
6. Some basic configuration need to be provided for the service. This window will be popped up after install. Sensor ID will be the ID of the speed sensor, which can be find out in the bike head unit/computer.
7. From the virtual power sensor data will start to flow to your bike head unit/computer as soon as it receives speed data from the sensor with the ID you've provided in the settings. Just do a scan on your device for power meters, it should show your new virtual power meter. The ID of the virtual power sensor will be the same for the same PI.
8. Disable SSH server or change password in your OSMC to prevent unauthorized access.

## Build addon

The current version of the addon is prebuilt in the dist directory. To build a new version, run the `build_addon.sh` script.