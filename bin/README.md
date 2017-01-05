# Scripts
This folder holds all scripts used by HA/Github/Travis/...

## Travis CI
The following scripts are used by Travis, when a commit has been done, Travis will start installing it's environment and run some scripts.

### [Dummy Secret](dummy_secrets.yaml)
This script is run as an installation step, after installing HA.
It will create a secrets file with all the currently used secrets entries used by the configuration.
This prevents the config checking failing on missing secrets entries.

### [Check Config](check_config.yaml)
This script is used as the actual checking of the config. It runs the HA config check command and processes the output.
If the output contains the keyword `ERROR`, it will exit the build with an error code, causing Travis to fail.

## Home Assistant
The following scripts are used by HA itself.

### [Get Commits](getcommits.yaml)
This script is used as a `command_line` sensor. It checks how many commits the local repository is behind on the origin one (Github).
It is planned that this sensor will be used in automation to autoupdate and autorestart HA.

### [Pull Config](pullconfig.yaml)
This script is the actual updating script of HA. It pulls the latest changes from the Github repo, and calls the HA restart service afterwards.
Currently this is represented by a button on the UI, but it will be extended to be automatically called based on the `getcommits` script

## Other
### [Start Hass](start-hass.yaml)
This script is to simplify the starting of HA, when it crashed, server restarted, any other unexpected thing happened.
It simply calls the HA script with the `hass` user in `daemon` mode.
