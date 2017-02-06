import voluptuous as vol

from homeassistant.components.binary_sensor import (
BinarySensorDevice, PLATFORM_SCHEMA)
from homeassistant.const import (
    CONF_NAME, CONF_PASSWORD, CONF_HOST)
import homeassistant.helpers.config_validation as cv

import logging
from datetime import timedelta
from homeassistant.util import Throttle
import requests

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOST, default='http://localhost:5050/api/'): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    password = config.get(CONF_PASSWORD)

    try:
        r = requests.get(host + 'status/', auth=('flexget', password))
    except requests.exceptions.RequestException:
        _LOGGER.error("Failed to connect to the configured Flexget instance")
        return False

    if(r.status_code == 401):
        _LOGGER.error("Authentication with Flexget failed")
        return False
    
    add_devices([FlexgetTaskSensor(task) for task in r.json()])

class FlexgetTaskSensor(BinarySensorDevice):
    """Representation of a Sensor."""
    def __init__(self, task):
        self._name = task['name']
        self._id = task['id']
        self._state = False
        self._last_execution = task['last_execution']
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def state_attributes(self):
        """Return the last execution details"""
        return self._last_execution

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
          """Get the latest data and updates the state and """
          print('getting update')
