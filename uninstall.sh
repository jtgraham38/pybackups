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

#remove repo at /opt/pybackups
rm -rf /opt/pybackups
if [ $? -eq 0 ]; then
    echo "'/opt/pybackups' removed"; 
else 
    echo "removal of '/opt/pybackups' failed"; 
fi   

#remove state at /var/lib/pybackups
rm -rf /var/lib/pybackups
if [ $? -eq 0 ]; then
    echo "'/var/lib/pybackups' removed"; 
else 
    echo "removal of '/var/lib/pybackups' failed"; 
fi   

#remove config at /etc/pybackups
rm -rf /etc/pybackups
if [ $? -eq 0 ]; then
    echo "'/etc/pybackups' removed"; 
else 
    echo "removal of '/etc/pybackups' failed"; 
fi   