#!/bin/bash

cd "/home/hass/.homeassistant"
git add known_devices.yaml
git commit -m "New device from server"
git push
