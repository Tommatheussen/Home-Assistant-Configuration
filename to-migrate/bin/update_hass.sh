#!/bin/bash

#Stop HA
service hass-daemon stop

source /PlexMediaServer/hass/bin/activate
pip3 install -U homeassistant

service hass-daemon start
