#!/bin/bash

#determine if we are running debian (raspi os basis)
if [ -f "/etc/debian_version" ]; then
    echo "Debian-based"; 
else 
    echo "Not Debian-based"; 
    exit;
fi   

#determine if git and python3 and pip are installed
#git
git --version
if [ $? -eq 0 ]; then
    echo "Git is installed"; 
else 
    echo "Git is not installed"; 
    exit;
fi   

#python
python --version
if [ $? -eq 0 ]; then
    echo "Python is installed"; 
else 
    echo "Python is not installed"; 
    exit;
fi    

#pip
pip --version
if [ $? -eq 0 ]; then
    echo "Pip is installed"; 
else 
    echo "Pip is not installed"; 
    exit;
fi    

#clone repo to /opt/pybackups
git clone https://github.com/jtgraham38/pybackups.git /opt/pybackups
if [ $? -ne 0 ]; then
    echo "pybackups clone failed, exiting"; 
    exit;
fi

#make service based on /opt/pybackups/service/pybackups.service
cp /opt/pybackups/service/pybackups.service  /etc/systemd/system/pybackups.service
if [ $? -ne 0 ]; then
    echo "copying service file from '/opt/pybackups/service/pybackups.service' to '/etc/systemd/system/pybackups.service' failed, exiting"; 
    exit;
fi

systemctl daemon-reload
systemctl enable --now pybackups.service
if [ $? -ne 0 ]; then
    echo "enabling service 'pybackups.service' failed, exiting"; 
    exit;
fi