#!/bin/bash

SERVER="$HOME/projects/SensorSend/backend/server.py"

/usr/bin/python3 "$SERVER" &
S_ID=$!

/usr/bin/chromium-browser --kiosk "file:///$HOME/projects/SensorSend/ui/index.html"

kill $S_ID