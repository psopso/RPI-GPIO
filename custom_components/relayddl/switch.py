from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.switch import PLATFORM_SCHEMA

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .relayddl import switch_on
from .relayddl import switch_off
from .relayddl import switch_is_on

CONF_I2C_ADDRESS = "i2c_address"
DEFAULT_I2C_ADDRESS = 0x10
CONF_PINS = "pins"


_SWITCHES_SCHEMA = vol.Schema({cv.positive_int: cv.string})
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PINS): _SWITCHES_SCHEMA,
        vol.Optional(CONF_I2C_ADDRESS, default=DEFAULT_I2C_ADDRESS): vol.Coerce(int),
    }
)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    switches = []
    pins = config.get(CONF_PINS)
    device = config.get(CONF_I2C_ADDRESS)
    for pin_num, pin_name in pins.items():
        switches.append(MySwitch(device, pin_name,pin_num))
    add_entities(switches)    

class MySwitch(SwitchEntity):
    def __init__(self, device, name, pin):
        self._is_on = False
        self._device = device
        self._name = name or DEVICE_DEFAULT_NAME
        self._pin = pin

    @property
    def name(self):
        """Name of the entity."""
        return self._name

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        self._is_on = switch_is_on(self._device, self._pin)
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        switch_on(self._device, self._pin)

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        switch_off(self._device, self._pin)
        self._is_on = False
