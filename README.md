# :house_with_garden: Home Assistant Configuration
## About
My repo containing all configuration for my Home Assistant.

## House Setup
We recently (2019) build a new house from scratch, this allowed me to make a strong backbone for the smartness in my house. As I had some previous experience with the KNX ecosystem, I've chosen this protocol for the backbone of the house. The basic idea boils down to the fact that my KNX installation is setup in a way that allows it to work with most of the house by itself, without Home Assistant even needing to run.
Visualisation in KNX gets very expensive very quickly, and connection to various other systems rack up prices very quickly, as they usually all need some kind of gateway to connect to the KNX bus.

Home Assistant is used as a secondary layer, adding all smartness into the house. If it were to go down for some reason, my house would still function with lights, sockets and ventilation as they are all tied into KNX.

# KNX Specific
## Problems and solutions
With this setup, I did encounter some minor 'problems' though. Mainly due to some limitations in the KNX modules I use, below is a list of issues I came accross, and how I solved them:

### Turning the lights on
In the beginning, there was no problem as Home Assistant was not set up yet, however after a while, I wanted to get circadian lighting up and running. The modules (basically LED drivers which can be controlled via KNX) I use for lighting inside KNX have a couple of options:
- A fixed value (eg 20%)
- Memory, sets the same value from before the light got turned off
- Max value (you can set the maximum value for a light)
- Different values for Day/Night cycle

While in most systems these options would perfectly suffice, I had a problem on my hand, seeing as none of the options are actually perfect for my solution.
If I were to use Memory, then lights that would have been turned off during the day, would come on at full brightness during the night, and then quickly dimming down, resulting in a bright flash before going to the correct circadian settings. The same happen with Max value, as all my lights have a maximum value of 100% right now. In some places I use the Day/night cycle, but these are also just static values.

I have settled on the Fixed value right now, the modules itself have a minimum value of 6%, I guess the drivers can't properly function below that. And it turns out, this is pretty much perfect. Now all my lights go to a value of 6%, that doesn't sounds like a lot but for LED lights it certainly is enough. As long as Home Assistant is running, the circadian lighting kicks in instantly and brightens up the lights where needed. If Home Assistant is down, I at least still have light (albeit not a lot) everywhere.

### Ventilation
I have not found a lot of time to fully investigate and identify the actual issue here, but it seems my ventilation system does not expose the correct values to the KNX bus. What this means is that I cannot use the standard Fan integration in Home Assistant to actually set the ventilation system and change the speeds.
For now, I have found that my ventilation system does support a Switch sensor for each speed setting, so I now have a couple of Switches in Home Assistant to change the speed of the ventilation, as well as some automations to toggle the correct switches.
The good thing, is that the ventilation automatically toggles the other speed switches off, so I only need to turn 1 on and the rest will go back to off.

I don't like this approach, because it's a lot harder to get this to work inside lovelace with fan cards and such, but it works for now, I will probably revise this in the future.
