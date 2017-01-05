#!/bin/bash

result = $(hass --config $TRAVIS_BUILD_DIR --script check_config)
echo result
