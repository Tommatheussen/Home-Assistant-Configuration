# :construction: :house: New configuration under construction...

# :house_with_garden: Home Assistant Configuration

## About
My repo containing all configuration for my Home Assistant.

## House Setup
We recently build a new house from scratch, this allowed me to make a strong backbone for the smartness in my house. As I had some previous experience with the KNX ecosystem, I've chosen this protocol for the backbone of the house. The basic idea boils down to the fact that my KNX installation is setup in a way that allows it to work with most of the house by itself, without Home Assistant even needing to run.
Visualisation in KNX gets very expensive very quickly, and connection to various other systems rack up prices very quickly, as they usually all need some kind of gateway to connect to the KNX bus.

Home Assistant is used as a secondary layer, adding all smartness into the house.




## Old stuff, still to be removed :no_mouth:
This is my configuration file for the awesome [Home Assistant](https://home-assistant.io).

It currently is a WIP, since there are a number of things left to do.

The way I use this repo is in the following steps:

1. Create a change in 1 or multiple files (through browser or other), on a seperate branch (master is protected).
2. Create a PR against master with the changes.
3. Travis runs on the PR branch, checking wether the config is correct. Travis installs HA and runs the command `hass --script check_config` for this.
4. After Travis builds successfully (and I've done all changes), I'll merge the PR (squashing the commits in my case, to keep the master branch commits cleaner).
5. On my HA instance I click my update button (which pulls new commits from master, and calls the service to restart HA).
6. Profit!
