#!/bin/bash

result=$(hass --config $TRAVIS_BUILD_DIR --script check_config)

echo "$result"
if [[ $result == *"ERROR"* ]]
then
  exit 1
fi

exit
