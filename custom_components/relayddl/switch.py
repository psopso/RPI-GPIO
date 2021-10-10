from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import CONF_ADDRESS, CONF_NAME, DEVICE_DEFAULT_NAME

import time as time
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .relayddl import switch_on
from .relayddl import switch_off
from .relayddl import switch_is_on

CONF_I2C_ADDRESS = "i2c_address"
DEFAULT_I2C_ADDRESS = 0x10
CONF_PINS = "pins"
CONF_CHANNELS = "channels"
CONF_INDEX = "index"
CONF_INVERT_LOGIC = "invert_logic"
CONF_INITIAL_STATE = "initial_state"
CONF_MOMENTARY = "momentary"

_CHANNELS_SCHEMA = vol.Schema(
    [
        {
            vol.Required(CONF_INDEX): cv.positive_int,
            vol.Required(CONF_NAME): cv.string,
            vol.Optional(CONF_INITIAL_STATE, default=False): cv.boolean,
            vol.Optional(CONF_MOMENTARY, default=0): cv.positive_int,
    }
    ]
)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_I2C_ADDRESS, default=DEFAULT_I2C_ADDRESS): vol.Coerce(int),
        vol.Required(CONF_CHANNELS): _CHANNELS_SCHEMA,
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
    device = config.get(CONF_I2C_ADDRESS)
    channels = config.get(CONF_CHANNELS)
    for channel_config in channels:
      ind = channel_config[CONF_INDEX]
      name = channel_config[CONF_NAME]
      init = channel_config[CONF_INITIAL_STATE]
      momentary = channel_config[CONF_MOMENTARY]
      switches.append(MySwitch(device,ind,name,init,momentary))

    add_entities(switches)

class MySwitch(SwitchEntity):
    def __init__(self, device, ind, name, init, momentary):
        self._is_on = False
        self._device = device
        self._ind = ind + 1
        self._name = name or DEVICE_DEFAULT_NAME
        self._init = init
        self._momentary = momentary

        if init:
          switch_on(self._device, self._ind, 0)
        else:
          switch_off(self._device, self._ind, 0)

    @property
    def name(self):
        """Name of the entity."""
        return self._name

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        self._is_on = switch_is_on(self._device, self._ind)
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        switch_on(self._device, self._ind, self._momentary)
        if self._momentary > 0:
          time.sleep(0.1*self._momentary)
          self.turn_off()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        switch_off(self._device, self._ind, self._momentary)
        self._is_on = False
