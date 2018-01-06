"""
Demo light platform that implements lights.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/demo/
"""
import random

from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, ATTR_EFFECT, ATTR_HS_COLOR,
    ATTR_WHITE_VALUE, SUPPORT_BRIGHTNESS, SUPPORT_COLOR_TEMP, SUPPORT_EFFECT,
    SUPPORT_COLOR, SUPPORT_WHITE_VALUE, Light)

LIGHT_COLORS = [
    (10226, 219),
    (62805, 192),
]

LIGHT_EFFECT_LIST = ['rainbow', 'none']

LIGHT_TEMPS = [240, 380]

SUPPORT_DEMO = (SUPPORT_BRIGHTNESS | SUPPORT_COLOR_TEMP | SUPPORT_EFFECT |
                SUPPORT_COLOR | SUPPORT_WHITE_VALUE)


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the demo light platform."""
    add_devices_callback([
        DemoLight("Bed Light", False, True, effect_list=LIGHT_EFFECT_LIST,
                  effect=LIGHT_EFFECT_LIST[0]),
        DemoLight("Ceiling Lights", True, True,
                  LIGHT_COLORS[0], LIGHT_TEMPS[1]),
        DemoLight("Kitchen Lights", True, True,
                  LIGHT_COLORS[1], LIGHT_TEMPS[0])
    ])


class DemoLight(Light):
    """Representation of a demo light."""

    def __init__(self, name, state, available=False, hs_color=None, ct=None,
                 brightness=180, white=200, effect_list=None, effect=None):
        """Initialize the light."""
        self._name = name
        self._state = state
        self._hs_color = hs_color
        self._ct = ct or random.choice(LIGHT_TEMPS)
        self._brightness = brightness
        self._white = white
        self._effect_list = effect_list
        self._effect = effect

    @property
    def should_poll(self) -> bool:
        """No polling needed for a demo light."""
        return False

    @property
    def name(self) -> str:
        """Return the name of the light if any."""
        return self._name

    @property
    def available(self) -> bool:
        """Return availability."""
        # This demo light is always available, but well-behaving components
        # should implement this to inform Home Assistant accordingly.
        return True

    @property
    def brightness(self) -> int:
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def hs_color(self) -> tuple:
        """Return the hs color value."""
        return self._hs_color

    @property
    def color_temp(self) -> int:
        """Return the CT color temperature."""
        return self._ct

    @property
    def white_value(self) -> int:
        """Return the white value of this light between 0..255."""
        return self._white

    @property
    def effect_list(self) -> list:
        """Return the list of supported effects."""
        return self._effect_list

    @property
    def effect(self) -> str:
        """Return the current effect."""
        return self._effect

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self._state

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_DEMO

    def turn_on(self, **kwargs) -> None:
        """Turn the light on."""
        self._state = True

        if ATTR_HS_COLOR in kwargs:
            self._hs_color = kwargs[ATTR_HS_COLOR]

        if ATTR_COLOR_TEMP in kwargs:
            self._ct = kwargs[ATTR_COLOR_TEMP]

        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]

        if ATTR_WHITE_VALUE in kwargs:
            self._white = kwargs[ATTR_WHITE_VALUE]

        if ATTR_EFFECT in kwargs:
            self._effect = kwargs[ATTR_EFFECT]

        # As we have disabled polling, we need to inform
        # Home Assistant about updates in our state ourselves.
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs) -> None:
        """Turn the light off."""
        self._state = False

        # As we have disabled polling, we need to inform
        # Home Assistant about updates in our state ourselves.
        self.schedule_update_ha_state()
