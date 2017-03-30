DOMAIN = 'counter'

CONF_SENSOR = 'sensor'

def setup(hass, config):
    """Setup the sensor platform."""
    sensor_name = DOMAIN + '.' + config[DOMAIN].get(CONF_SENSOR, 'default')
    hass.states.set(sensor_name, 0)

    def handle_increment(call):
        state = hass.states.get(sensor_name)
        new_state = int(state.state) + 1
        hass.states.set(sensor_name, new_state)

    def handle_reset(call):
        hass.states.set(sensor_name, 0)

    hass.services.register(DOMAIN, 'increment', handle_increment)
    hass.services.register(DOMAIN, 'reset', handle_reset)
    return True
