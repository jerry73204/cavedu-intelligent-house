#!/bin/bash
LOG_PATH="/var/log/cavedu_house.log"
while true; do sleep 1; [ "$(wc -l $LOG_PATH | cut -d' ' -f1)" -gt 50000 ] && rm "$LOG_PATH"; done &
(/bin/date; /usr/bin/node /root/app/app.js) &>> "$LOG_PATH" &
