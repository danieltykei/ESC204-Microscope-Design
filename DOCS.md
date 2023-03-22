# Team Documentation

## Goal
We want this repository to contained backed up, version tracked, accessible code to facilitate prototyping.

## Guidelines
1. ```code.py``` should only import other modules and define a routine for the device used. Do not define functions or otherwise, instead use other files that can be imported.
1. Indicate if your code is for raspberry pi pico, RP4 or arduino nano in the filename.
1. Comment your code, should say 'why' not 'what'.
1. Report issues in the issues tab as they arise. This to keep a papertrail of bugs and how we solve them.

## Circuit Python (Pico/Nano)
Reminder in case BOOTSEL is double tapped
1. Download appropriate ```uf2``` file
1. Drag and drop into microcontroller to flash

## Raspberry Pi 4
1. Materials
    - Raspberry Pi (Here model 4B is used)
    - SD card or USB (recommended minimum 8GB, also faster is better for reading/writing data)
    - USB-C cable to power the RP4
    - Ethernet Cable
1. Software
    - Raspbian OS Imager
    - VNC viewer (RealVNC or your preferred viewer)
    - Terminal
1. Setup
    - Gather materials/Software
    - Flash Raspbian OS onto the SD/USB
        - WARNING this process will reformat your drive, make sure to backup the data on it first
        - Plug in SD/USB and unplug all other USB/SD cards to avoid confusion
        - Run the imager software, select the recommended OS with desktop and select your drive
        - In settings, enable SSH and set a username/password (write this down somewhere secure)
        - Flashing the OS will take a few minutes
1. Logging in
    - Connect the SD/USB into the RP4, then the ethernet and power cables (troubleshoot LED signals here)
    - Open terminal and execute ```ssh <username>@raspberrypi.local``` and enter password (ping raspberrypi.local to troubleshoot)
    - Execute ```raspi-config``` and enable VNC
    - Open VNC software and connect to ```raspberrypi.local```

## PiCamera
## Stepper Motor
