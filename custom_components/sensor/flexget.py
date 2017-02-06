from homeassistant.helpers.entity import Entity
from homeassistant.const import (CONF_NAME, CONF_PASSWORD, CONF_HOST)
import logging
import time
from datetime import timedelta
from homeassistant.util import Throttle
import requests

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=15)

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    password = config.get(CONF_PASSWORD)
    
    r = requests.get(host + '/status/', auth=('flexget', password))
    print(r.json())
        
    #add_devices([FlexgetTaskSensor()])


class ExampleSensor(Entity):
    """Representation of a Sensor."""
    def __init(self, name):
    	self._state = None
    	self._name = name

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Example Temperature'

    @property
    def state(self):
        """Return the state of the sensor."""
        return 23

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS
        
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
    	  """Get the latest data and updates the state and """
