# :construction: :house: New configuration under construction...

# Home-Assistant-Configuration

This is my configuration file for the awesome [Home Assistant](https://home-assistant.io).

It currently is a WIP, since there are a number of things left to do.

The way I use this repo is in the following steps:

1. Create a change in 1 or multiple files (through browser or other), on a seperate branch (master is protected).
2. Create a PR against master with the changes.
3. Travis runs on the PR branch, checking wether the config is correct. Travis installs HA and runs the command `hass --script check_config` for this.
4. After Travis builds successfully (and I've done all changes), I'll merge the PR (squashing the commits in my case, to keep the master branch commits cleaner).
5. On my HA instance I click my update button (which pulls new commits from master, and calls the service to restart HA).
6. Profit!
