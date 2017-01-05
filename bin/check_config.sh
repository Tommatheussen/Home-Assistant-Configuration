#!/bin/bash

result=`hass --config $TRAVIS_BUILD_DIR --script check_config`

if [[ $result == *"Failed"* ]]
then
  exit 1
fi

exit
