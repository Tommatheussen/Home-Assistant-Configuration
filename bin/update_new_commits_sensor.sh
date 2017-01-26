#!/bin/bash

cd "/home/hass/.homeassistant"
git fetch
commits="$(git rev-list --count master..origin/master)"

curl -X POST -H "x-ha-access: $1" -H "Content-Type: application/json" https://matheussen.serverpit.com:8123/api/states/sensor.new_commits -d "{\"state\": $commits}"
