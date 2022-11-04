# SensorSend

This is a basic flask server that waits for an incoming request and will read from sensors and return the values to the client. Inside of the collection it will also send the data via mqtt to a broker so other services can have the data too. Currently a local host local html page will contact the server every 2 seconds or so to get the data.

## Desktop Entry
Create in ~/Desktop a file like Temp.desktop.
```
[Desktop Entry]
Version=1.0
Type=Application
Encoding=UTF-8
Name=Temp Display
Comment=Temperature Display
# Icon=/home/pi/Downloads/icon.png
# Exec=/usr/bin/chromium-browser --kiosk file:///home/pi/projects/SensorSend/ui/index.html
Exec=/home/pi/projects/SensorSend/run.sh
Terminal=false
Categories=Graphics
```

## Auto Start on Boot
```
# This is the way it would work for Raspberry Pi OS
sudo ln -s /home/pi/Desktop/Temp.desktop /etc/xdg/autostart
```