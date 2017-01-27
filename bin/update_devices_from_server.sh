#!/bin/bash

cd "/home/hass/.homeassistant"
git add known_devices.yaml
git commit -m "New device from server"

result="$(git push)"

curl --verbose -X POST -H "x-ha-access: $1" -H "Content-Type: application/json" https://matheussen.serverpit.com:8123/api/events/device_failed -d "{\"reason\": \"$result\"}"
