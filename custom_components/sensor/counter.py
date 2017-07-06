import logging
from datetime import timedelta

import voluptuous as vol

from homeassistant.components.sensor import DOMAIN, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_INITIAL = 'initial'
CONF_STEP = 'step'

DEFAULT_NAME = 'Counter'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_INITIAL, default=0): vol.Coerce(int),
    vol.Optional(CONF_STEP, default=1): vol.Coerce(int)
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    data = CounterData(hass, config)
    sensor = CounterSensor(data, config.get(CONF_NAME))
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
    def __init__(self, counter_data, name):
        self.counter_client = counter_data
        self._state = self.counter_client.count
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        self._state = self.counter_client.count

class CounterData(object):
    """Keep all counter data and actions."""
    
    def __init__(self, hass, config):
        self._initial = config[CONF_INITIAL]
        self._step = config[CONF_STEP]
        self.count = self._initial

    def increment(self):
        _LOGGER.info('Incrementing counter')
        self.count += self._step

    def reset(self):
        _LOGGER.info('Resetting counter')
        self.count = self._initial

    def decrement(self):
        _LOGGER.info('Decrementing counter')
        self.count -= self._step
