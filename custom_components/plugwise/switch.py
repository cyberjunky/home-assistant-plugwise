"""
Support for plugwise circles.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.plugwise/
"""
import logging
import voluptuous as vol
import plugwise
from plugwise import TimeoutException

from homeassistant.const import (CONF_PORT)
import homeassistant.helpers.config_validation as cv
from homeassistant.const import STATE_UNKNOWN
from serial.serialutil import SerialException

try:
    from homeassistant.components.switch import (SwitchEntity, PLATFORM_SCHEMA)
except ImportError:
    from homeassistant.components.switch import (SwitchDevice as SwitchEntity, PLATFORM_SCHEMA)

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = '/dev/ttyUSB0'
CONF_CIRCLES = "circles"

ATTR_CURRENT_CONSUMPTION = 'current_consumption'
ATTR_CURRENT_CONSUMPTION_UNIT = 'current_consumption_unit'
ATTR_CURRENT_CONSUMPTION_UNIT_VALUE = 'W'

ATTR_FW_VERSION = 'firmware_version'
ATTR_DATE_TIME = 'date_time'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.string,
    vol.Required(CONF_CIRCLES): {cv.string: cv.string},
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup Plugwise."""
    # Connect to the plugwise stick
    try:
        stick = plugwise.Stick(config.get(CONF_PORT))
        _LOGGER.info("Connected to Plugwise stick")
    except (TimeoutException):
        _LOGGER.error("Timeout occured while connecting to Plugwise stick")
        return
    except Exception as err:
        _LOGGER.error("Unknown error occured while connecting to Plugwise stick: %s" % err)
        return

    # Add all circles to hass
    for name, mac in config[CONF_CIRCLES].items():
        data = PlugwiseSwitchData(stick, mac)
        add_devices([PlugwiseSwitch(hass, data, name)], True)
        _LOGGER.info("Created Plugwise switch for Circle: %s", name)


class PlugwiseSwitch(SwitchEntity):
    """Representation of a plugwise switch."""

    def __init__(self, hass, data, name):
        """Initialize the switch."""
        self.data = data
        self._name = name

    @property
    def name(self):
        """Return the name of the switch, if any."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attrs = {}

        if self.data.current_consumption != STATE_UNKNOWN:
            attrs[ATTR_CURRENT_CONSUMPTION] = "{:.1f}".format(
                self.data.current_consumption)
            attrs[ATTR_CURRENT_CONSUMPTION_UNIT] = "{}".format(
                ATTR_CURRENT_CONSUMPTION_UNIT_VALUE)

        attrs[ATTR_FW_VERSION] = self.data.fwversion
        attrs[ATTR_DATE_TIME] = self.data.datetime

        return attrs

    @property
    def current_power_watt(self):
        """Return the current power usage in Watt."""
        try:
            return float(self.data.current_consumption)
        except ValueError:
            return None

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.data.state

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self.data.switch_on()

    def turn_off(self):
        """Turn the switch off."""
        self.data.switch_off()

    def update(self):
        """Get the latest data from the plugwise."""
        self.data.update()


class PlugwiseSwitchData(object):
    """Get the latest data from plugwise circles."""

    def __init__(self, stick, mac):
        """Initialize the data object."""
        self.getinfo = None
        self.fwversion = None
        self.datetime = None
        self.state = STATE_UNKNOWN
        self.current_consumption = STATE_UNKNOWN

        self._circle = plugwise.Circle(mac, stick)

    def update(self):
        """Get the latest data from the plugwise circles."""

        try:
            self.getinfo = self._circle.get_info()
            self.current_consumption = self._circle.get_power_usage()
        except (TimeoutException):
            _LOGGER.error("Timeout occured while getting data from circle")
            return
        except Exception as err:
            _LOGGER.error("Unknown error occured while getting data from circle: %s" % err)
            return

        self.state = self.getinfo['relay_state']
        self.fwversion = self.getinfo['fw_ver']
        self.datetime = self.getinfo['datetime']
        _LOGGER.debug("Current Consumption: %s", self.current_consumption)
        _LOGGER.debug("Relay State: %s", self.state)
        return

    def switch_on(self):
        """Turn the switch on."""
        self._circle.switch_on()

    def switch_off(self):
        """Turn the switch off."""
        self._circle.switch_off()
