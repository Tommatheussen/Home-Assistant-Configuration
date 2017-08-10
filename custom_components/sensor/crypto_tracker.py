import logging
from datetime import timedelta

from homeassistant.helpers.entity import Entity

REQUIREMENTS = ['cryptonator==0.0.2']

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

CONF_BASE = 'base'
CONF_COINS = 'coins'

def setup_platform(hass, config, add_devices, discover_info=None):
    """Setup the crypto_tracker component."""
    # States are in the format DOMAIN.OBJECT_ID.
    import cryptonator

    base = config.get(CONF_BASE)
    coins = config.get(CONF_COINS)

    unique_coins = []
    for coin in coins:
      if coin.get('token') not in unique_coins:
        unique_coins.append(coin.get('token'))

    crypto = cryptonator.Cryptonator()

    add_devices([CryptoTracker(crypto, base, coins, unique_coins)], True)

class CryptoTracker(Entity):
    """Representation of the Crypto Tracker."""

    def __init__(self, crypto, base, coins, unique_coins):
        """Initialize the cryptotracker."""
        self._state = 0
        self._crypto = crypto
        self._base = base
        self._coins = coins
        self._unique_coins = unique_coins

    @property
    def name(self):
        return 'Crypto Tracker'

    @property
    def unit_of_measurement(self):
        return self._base

    @property
    def state(self):
        return self._state

    def update(self):
      prices = self._crypto.get_exchange_rates(self._base, self._unique_coins)

      initialprice = 0
      endprice = 0
      for coin in self._coins:
        if coin.get('token') in prices and prices.get(coin.get('token')) is not None:
          initialprice += coin.get('amount') * coin.get('price')
          endprice += coin.get('amount') / prices.get(coin.get('token'))

      self._state = endprice - initialprice
