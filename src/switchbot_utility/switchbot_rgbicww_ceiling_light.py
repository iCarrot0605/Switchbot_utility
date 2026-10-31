from switchbot_utility.onoff_mixin import OnOffMixin
from switchbot_utility.switchbot_device import SwitchbotDevice


class SwitchbotRGBICWWCeilingLight(SwitchbotDevice, OnOffMixin):
    """Switchbot RGBICWW Ceiling Light class"""

    def __init__(self, deviceId):
        """Constructor"""
        super().__init__(deviceId)

    def toggle(self) -> str:
        """Toggle state"""
        self._body["command"] = "toggle"
        result = self.command(self.deviceId, self._body)
        return result.text

    def turn_on_main_light(self) -> str:
        """Turn on main light"""
        self._body["command"] = "turnOnMainLight"
        result = self.command(self.deviceId, self._body)
        return result.text

    def turn_off_main_light(self) -> str:
        """Turn off main light"""
        self._body["command"] = "turnOffMainLight"
        result = self.command(self.deviceId, self._body)
        return result.text

    def turn_on_color_light(self) -> str:
        """Turn on color light"""
        self._body["command"] = "turnOnColorLight"
        result = self.command(self.deviceId, self._body)
        return result.text

    def turn_off_color_light(self) -> str:
        """Turn off color light"""
        self._body["command"] = "turnOffColorLight"
        result = self.command(self.deviceId, self._body)
        return result.text

    def set_main_light_brightness(self, brightness: int) -> str:
        """Set main light brightness(1-100)"""
        self._body["command"] = "setMainLightBrightness"
        self._body["parameter"] = brightness
        result = self.command(self.deviceId, self._body)
        return result.text

    def set_main_light_color_temperature(self, temperature: int) -> str:
        """Set main light color temperature(2700-6500)"""
        self._body["command"] = "setMainLightColorTemp"
        self._body["parameter"] = temperature
        result = self.command(self.deviceId, self._body)
        return result.text

    def set_color_light_brightness(self, brightness: int) -> str:
        """Set color light brightness(1-100)"""
        self._body["command"] = "setColorLightBrightness"
        self._body["parameter"] = brightness
        result = self.command(self.deviceId, self._body)
        return result.text

    def set_color_light_rgb(self, r: int, g: int, b: int) -> str:
        """Set color light RGB

        args: r_value, g_value, b_value 0-255"""
        self._body["command"] = "setColor"
        self._body["parameter"] = "{}:{}:{}".format(r, g, b)
        result = self.command(self.deviceId, self._body)
        return result.text

    def get_power(self) -> str:
        """Total power state on, off, partial"""
        status = self.get_status()
        return status["power"]

    def get_online_status(self) -> str:
        """Returns connection status. online or offline"""
        status = self.get_status()
        return status["onlineStatus"]

    def get_main_light_power(self) -> str:
        """Returns main light power state on or off"""
        status = self.get_status()
        return status["mainLightPower"]

    def get_main_light_brightness(self) -> int:
        """Returns the brightness value, range from 1 to 100"""
        status = self.get_status()
        return status["mainLightBrightness"]

    def get_main_light_color_temperature(self) -> int:
        """Returns the color temperature value, range from 2700 to 6500"""
        status = self.get_status()
        return status["mainLightColorTemp"]

    def get_color_light_power(self) -> str:
        """Returns color light power state on or off"""
        status = self.get_status()
        return status["colorLightPower"]

    def get_color_light_brightness(self) -> int:
        """Returns the brightness value, range from 1 to 100"""
        status = self.get_status()
        return status["colorLightBrightness"]

    def get_color_light_rgb(self) -> str:
        """Returns the color value, RGB '255:255:255'"""
        status = self.get_status()
        return status["colorLightRGB"]
