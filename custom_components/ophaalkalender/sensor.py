"""
Sensor component for waste pickup dates from belgium waste collectors
Original Author: Pippijn Stortelder
Current Version: 1.1.3 20191118 - Pippijn Stortelder
20190207 - Changed Groenafval to GFT
20190218 - Fixed typo
20190223 - Fix for HA 88
20190611 - HACS compatible
20190612 - Fixed HACS
20180822 - Fixed version numbering
20191118 - Include categories 'gemengde plastics' & 'pmd'
"""

import logging
from datetime import datetime
from datetime import timedelta
import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_RESOURCES)
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

__version__ = '1.1.2'

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)
CONF_STREET_NAME = 'streetname'
CONF_POSTCODE = 'postcode'
CONF_STREET_NUMBER = 'streetnumber'
CONF_DATE_FORMAT = 'dateformat'
CONF_TODAY_TOMORROW = 'upcomingsensor'
CONF_DATE_ONLY = 'dateonly'

ATTR_OFFICIAL_NAME = 'Official name'
ATTR_WASTE_COLLECTOR = 'wastecollector'
ATTR_FRACTION_ID = 'ID'
ATTR_LAST_UPDATE = 'Last update'
ATTR_HIDDEN = 'Hidden'

COLLECTOR_URL = {
    'ophaalkalender': 'https://www.ophaalkalender.be',
}

RENAME_TITLES = {
    'tuinafval': 'gft',
    'p-k': 'papier',
    'rest': 'restafval',
    'grof huisvuil': 'grofafval',
    'grof huisvuil afroep': 'grofafval',
    'gemengde plastics': 'plastic',
    'pmd': 'pmd',
}

# COLLECTOR_WASTE_ID = {}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_RESOURCES, default=[]): cv.ensure_list,
    vol.Required(CONF_STREET_NAME, default='straat'): cv.string,
    vol.Required(CONF_POSTCODE, default='1111'): cv.string,
    vol.Required(CONF_STREET_NUMBER, default='1'): cv.string,
    vol.Optional(CONF_DATE_FORMAT, default='%d-%m-%Y'): cv.string,
    vol.Optional(CONF_TODAY_TOMORROW, default=False): cv.boolean,
    vol.Optional(CONF_DATE_ONLY, default=False): cv.boolean,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug('Setup Rest API retriever')

    postcode = config.get(CONF_POSTCODE)
    street_name = config.get(CONF_STREET_NAME)
    street_number = config.get(CONF_STREET_NUMBER)
    waste_collector = 'ophaalkalender'
    date_format = config.get(CONF_DATE_FORMAT)
    date_only = config.get(CONF_DATE_ONLY)

    try:
        data = WasteData(postcode, street_name, street_number, waste_collector)
    except requests.exceptions.HTTPError as error:
        _LOGGER.error(error)
        return False

    entities = []

    for resource in config[CONF_RESOURCES]:
        sensor_type = resource.lower()
        entities.append(WasteSensor(data, sensor_type, waste_collector, date_format, date_only))

    add_entities(entities)


class WasteData(object):

    def __init__(self, postcode, street_name, street_number, waste_collector):
        self.data = None
        self.postcode = postcode
        self.street_name = street_name
        self.street_number = street_number
        self.waste_collector = waste_collector
        self.main_url = COLLECTOR_URL[self.waste_collector]

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        _LOGGER.debug('Updating Waste collection dates using Rest API')

        try:
            url = self.main_url + '/calendar/findstreets/?query=' + self.street_name + "&zipcode=" + self.postcode
            response = requests.get(url).json()

            if not response:
                _LOGGER.error('Address not found!')
            else:
                address_code = response[0]["Id"]
                url = self.main_url +  '/api/rides?id=' + str(address_code) + '&housenumber=' + \
                      self.street_number + '&zipcode=' + self.postcode
                request_json = requests.get(url).json()
                if not request_json:
                    _LOGGER.error('No Waste data found!')
                else:
                    sensor_dict = {}

                    for key in request_json:

                        if not key['start'] is None:
                            check_title = key['title'].lower()
                            title = ''

                            for dict_title in RENAME_TITLES:
                                if dict_title in check_title:
                                    title = RENAME_TITLES[dict_title]
                                    break
                            if not title:
                                title = check_title

                            if title in sensor_dict:
                                sensor_dict[title].append(datetime.strptime(key['start'].split("T")[0], '%Y-%m-%d'))
                            else:
                                sensor_dict[title] = [datetime.strptime(key['start'].split("T")[0], '%Y-%m-%d')]

                    self.data = sensor_dict

        except requests.exceptions.RequestException as exc:
            _LOGGER.error('Error occurred while fetching data: %r', exc)
            self.data = None
            return False


class WasteSensor(Entity):

    def __init__(self, data, sensor_type, waste_collector, date_format, date_only):
        self.data = data
        self.type = sensor_type
        self.waste_collector = waste_collector
        self.date_format = date_format
        self.date_only = date_only
        self._name = waste_collector + ' ' + self.type
        self._unit = ''
        self._hidden = False
        self._icon = 'mdi:recycle'
        self._state = None
        self._last_update = None

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return {
            ATTR_WASTE_COLLECTOR: self.waste_collector,
            ATTR_LAST_UPDATE: self._last_update,
            ATTR_HIDDEN: self._hidden
        }

    @property
    def unit_of_measurement(self):
        return self._unit

    def update(self):
        self.data.update()
        waste_data = self.data.data
        try:
            if waste_data:
                if self.type in waste_data:
                    today = datetime.today()
                    collection_date = self.get_next_collection(today, waste_data, self.type)
                    if collection_date:
                        self._last_update = today.strftime('%d-%m-%Y %H:%M')
                        date_diff = (collection_date - today).days + 1
                        self._hidden = False
                        if self.date_only:
                            if date_diff >= 0:
                                self._state = collection_date.strftime(self.date_format)
                        else:
                            if date_diff >= 8:
                                self._state = collection_date.strftime(self.date_format)
                            elif date_diff > 1:
                                self._state = collection_date.strftime('%A, ' + self.date_format)
                            elif date_diff == 1:
                                self._state = collection_date.strftime('Tomorrow, ' + self.date_format)
                            elif date_diff == 0:
                                self._state = collection_date.strftime('Today, ' + self.date_format)
                            else:
                                self._state = None

                    else:
                        self._state = None
                        self._hidden = True
                else:
                    self._state = None
                    self._hidden = True
        except ValueError:
            self._state = None
            self._hidden = True

    @staticmethod
    def get_next_collection(today, waste_dict, fraction):
        next_collection_date = None
        for collection_date in waste_dict[fraction]:
            if collection_date >= today.replace(hour=0, minute=0, second=0, microsecond=0):
                next_collection_date = collection_date
                break
        return next_collection_date
