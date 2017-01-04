#!/bin/bash

cd "/home/hass/.homeassistant"
git fetch
echo $(git rev-list --count master..origin/master)
exit
