#!/bin/bash

SERVER="$HOME/projects/SensorSend/backend/server.py"

sudo systemctl start sensorsend
/usr/bin/chromium-browser --kiosk "file:///$HOME/projects/SensorSend/ui/index.html"
