#disable the pybackups service temporarily
#remove service file at /etc/systemd/system/pybackups.service
systemctl stop pybackups
sudo systemctl disable pybackups.service
rm /etc/systemd/system/pybackups.service
if [ $? -eq 0 ]; then
    echo "'/etc/systemd/system/pybackups.service' removed"; 
else 
    echo "removal of '/etc/systemd/system/pybackups.service' failed"; 
fi   
systemctl daemon-reload

#pull down latest changes
cd /opt/pybackups && git pull   
if [ $? -eq 0 ]; then
    echo "pulling latest changes succeeded"; 
else 
    echo "pulling latest changes failed, exiting"; 
fi   

#re-init the service
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