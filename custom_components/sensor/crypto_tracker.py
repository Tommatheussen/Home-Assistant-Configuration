import logging
from datetime import timedelta

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['cryptonator==0.0.2']

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

CONF_BASE = 'base'
CONF_COINS = 'coins'

DEFAULT_NAME = 'Crypto Tracker'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_BASE): cv.string,
    vol.Required(CONF_COINS): cv.ensure_list,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
})

def setup_platform(hass, config, add_devices, discover_info=None):
    """Setup the crypto_tracker component."""
    import cryptonator

    base = config.get(CONF_BASE)
    coins = config.get(CONF_COINS)
    name = config.get(CONF_NAME)

    crypto = cryptonator.Cryptonator()

    add_devices([CryptoTracker(name, crypto, base, coins)], True)

class CryptoTracker(Entity):
    """Representation of the Crypto Tracker."""

    def __init__(self, name, crypto, base, coins):
        """Initialize the cryptotracker."""
        self._state = 0
        self._crypto = crypto
        self._base = base
        self._coins = coins
        self._name = name
        self._attributes = {}

        def get_unique_coins(self):
            self._unique_coins = []
            for coin in self._coins:
                if coin.get('token') not in self._unique_coins:
                    self._unique_coins.append(coin.get('token'))

        get_unique_coins(self)

    @property
    def name(self):
        return self._name

    @property
    def unit_of_measurement(self):
        return self._base

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return self._attributes

    def update(self):
      self._attributes = {}
      prices = self._crypto.get_exchange_rates(self._base, self._unique_coins)

      initialprice = 0
      endprice = 0
      for coin in self._coins:
        if coin.get('token') in prices and prices.get(coin.get('token')) is not None:
          coin_initial_price = coin.get('amount') * coin.get('price')
          coin_end_price = coin.get('amount') / prices.get(coin.get('token'))

          self._attributes[str(coin.get('token')) + '@' + str(coin.get('price'))] = coin_end_price - coin_initial_price
          initialprice += coin_initial_price
          endprice += coin_end_price

      self._state = endprice - initialprice

