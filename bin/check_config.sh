#!/bin/bash

result=$(hass --config $TRAVIS_BUILD_DIR --script check_config)

if [[ $result == *"ERROR"* ]]
then
  echo "$result"
  exit 1
fi

exit
