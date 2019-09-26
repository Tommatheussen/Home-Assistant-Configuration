#!/bin/bash

cd "/home/hass/.homeassistant"
git add known_devices.yaml
git commit -m "New device from server"
git push

if [ $? -ne 0 ]; then
  curl --verbose -X POST -H "x-ha-access: $1" -H "Content-Type: application/json" https://matheussen.serverpit.com:8123/api/events/update_device_from_server_failed
fi
