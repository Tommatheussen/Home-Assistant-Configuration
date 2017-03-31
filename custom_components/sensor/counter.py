import asyncio
import logging
import voluptuous as vol

from homeassistant.components.sensor import DOMAIN
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    data = CounterData(hass, config)
    sensor = CounterSensor(data)
    add_devices([sensor])

    def increment_counter(call=None):
        data.increment()
        sensor.update()

    def reset_counter(call=None):
        data.reset()
        sensor.update()

    def decrement_counter(call=None):
        data.decrement()
        sensor.update()

    hass.services.register(DOMAIN, 'increment_counter', increment_counter)
    hass.services.register(DOMAIN, 'reset_counter', reset_counter)
    hass.services.register(DOMAIN, 'decrement_counter', decrement_counter)

class CounterSensor(Entity):
    def __init__(self, counter_data):
        self._name = 'Counter'
        self.counter_client = counter_data
        self._state = None
       
    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
       	self._state = self.counter_client.count

class CounterData(object):
    """Keep all counter data and actions."""
    
    def __init__(self, hass, config):
        self.count = 0

    def increment(self):
        _LOGGER.info('Incrementing counter')
        self.count += 1

    def reset(self):
        _LOGGER.info('Resetting counter')
        self.count = 0

    def decrement(self):
        _LOGGER.info('Decrementing counter')
        self.count -= 1
