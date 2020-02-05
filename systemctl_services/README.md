# systemctl configuration
----
## Overview
This folder contains the scripts and unit files to configure two services.

----
## RaspCam service

This service is responsible to initiate the camera preview and RPC server:

Copy the file rpc.service to the systemd folder.

    sudo mv rpc.service /etc/systemd/system/

Copy the script RaspCamServer.py to the /usr/bin

    sudo mv RaspCamServer.py /usr/bin

Reload the available services:

    sudo systemctl daemon-reload

Enable the service to start with the system:

    sudo systemctl enable rpc.service

Start the service:

    sudo systemctl start rpc.service

----
## Chrome service

This service starts chromium in kiosk mode in the streamlit page:

Copy the file chrome.service to the systemd folder.

    sudo mv chrome.service /etc/systemd/system/

Copy the script testechrome.sh to the /usr/bin

    sudo mv testechrome.sh /usr/bin

Give permission to execute:

    sudo chmod +x testechrome.sh

Reload the available services:

    sudo systemctl daemon-reload

Enable the service to start with the system:

    sudo systemctl enable chrome.service

Start the service:

    sudo systemctl start chrome.service


