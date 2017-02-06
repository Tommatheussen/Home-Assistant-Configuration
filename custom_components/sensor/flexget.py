from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_NAME, CONF_PASSWORD, CONF_HOST)
import logging
import time
import voluptuous as vol
from datetime import timedelta
from homeassistant.util import Throttle
import requests

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=15)

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

class FlexgetTaskSensor(Entity):
    """Representation of a Sensor."""
    def __init__(self, task):
        self._name = task['name']
        self._last_execution = task['last_execution']
        print(task)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._last_execution['succeeded']

  #  @property
  #  def unit_of_measurement(self):
   #     """Return the unit of measurement."""
    #    return TEMP_CELSIUS
        
    #@Throttle(MIN_TIME_BETWEEN_UPDATES)
    #def update(self):
    #	  """Get the latest data and updates the state and """
