from switchbot_utility.onoff_mixin import OnOffMixin
from switchbot_utility.switchbot_device import SwitchbotDevice


class SwitchbotPermanentOutdoorLights(SwitchbotDevice, OnOffMixin):
    """Switchbot Permanent Outdoor Lights class"""

    def toggle(self) -> str:
        """Toggle state"""
        self._body["command"] = "toggle"
        result = self.command(self.deviceId, self._body)
        return result.text

    def set_brightness(self, brightness: int) -> str:
        """Set brightness(0-100)"""
        self._body["command"] = "setBrightness"
        self._body["parameter"] = brightness
        result = self.command(self.deviceId, self._body)
        return result.text

    def set_color(self, r: int, g: int, b: int) -> str:
        """Set color

        args: r_value, g_value, b_value 0-255"""
        self._body["command"] = "setColor"
        self._body["parameter"] = "{}:{}:{}".format(r, g, b)
        result = self.command(self.deviceId, self._body)
        return result.text

    def set_color_temperature(self, temperature: int) -> str:
        """Set color temperature

        args: temperature 2700-6500"""
        self._body["command"] = "setColorTemperature"
        self._body["parameter"] = temperature
        result = self.command(self.deviceId, self._body)
        return result.text

    def get_power(self) -> str:
        """Returns ON/OFF state"""
        status = self.get_status()
        return status["power"]

    def get_brightness(self) -> int:
        """Returns the brightness value, range from 1 to 100"""
        status = self.get_status()
        return status["brightness"]

    def get_color(self) -> str:
        """Returns the color value, RGB '255:255:255'"""
        status = self.get_status()
        return status["color"]

    def get_color_temperature(self) -> int:
        """Returns the color temperature value, range from 2700 to 6500"""
        status = self.get_status()
        return status["colorTemperature"]
