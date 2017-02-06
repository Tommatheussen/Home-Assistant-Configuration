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
    host = config.get(CONF_HOST)
    password = config.get(CONF_PASSWORD)

    try:
        r = requests.get(host + 'status/', auth=('flexget', password), params=({'include_execution': False }))
    except requests.exceptions.RequestException:
        _LOGGER.error("Failed to connect to the configured Flexget instance")
        return False

    if(r.status_code == 401):
        _LOGGER.error("Authentication with Flexget failed")
        return False
    
    add_devices([FlexgetTaskSensor(task['name'], task['id'], host, password) for task in r.json()])

class FlexgetTaskSensor(BinarySensorDevice):
    """Representation of a Sensor."""
    def __init__(self, name, task_id, host, password):
        self._name = name
        self._id = task_id
        self._host = host
        self._password = password
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._last_execution['succeeded']

    @property
    def state_attributes(self):
        """Return the last execution details"""
        return self._last_execution

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data and updates the state and """
        # TODO: handle errors
        r = requests.get(self._host + 'status/' + str(self._id) + '/', auth=('flexget', self._password))
        self._last_execution = r.json()['last_execution']