from switchbot_utility.switchbot_device import SwitchbotDevice
from switchbot_utility.onoff_mixin import OnOffMixin


class SwitchbotCirculatorFan(SwitchbotDevice, OnOffMixin):
    """Switchbot Circulator Fan class"""

    def get_power(self) -> str:
        """Return current state

        Returns:
            str: "on" or "off"
        """
        status = self.get_status()
        return status["power"]

    def get_mode(self) -> str:
        """Return the current mode

        Returns:
            direct mode: "direct"; natural mode: "natural"; sleep mode: "sleep"; ultra quiet mode: "baby"
        """
        status = self.get_status()
        return status["mode"]

    def get_nightStatus(self) -> str:
        """Get nightlight status

        Returns:
            str: turn off: off; mode 1: 1; mode 2: 2
        """
        status = self.get_status()
        return status["nightStatus"]

    def get_oscillation(self) -> str:
        """Get horizontal oscillation

        Returns:
            str: turn on: on; turn off: off
        """
        status = self.get_status()
        return status["oscillation"]

    def get_verticalOscillation(self) -> str:
        """Get vertical oscillation

        Returns:
            str: turn on: on; turn off: off
        """
        status = self.get_status()
        return status["verticalOscillation"]

    def get_fan_speed(self) -> int:
        """Get fan speed

        Returns:
            int: 1-100
        """
        status = self.get_status()
        return status["fanSpeed"]

    def set_NightLightMode(self, mode: str) -> str:
        """Set mode

        Args:
            off: turn off nightlight,1: bright 2: dim

        Returns:
            str: result
        """
        self._body["command"] = "setNightLightMode"
        self._body["parameter"] = mode
        result = self.command(self.deviceId, self._body)
        return result.text

    def set_wind_mode(self, mode: str) -> str:
        """Set mode

        Args:
            direct mode: "direct"; natural mode: "natural"; sleep mode: "sleep"; ultra quiet mode: "baby"

        Returns:
            str: result
        """
        self._body["command"] = "setWindMode"
        self._body["parameter"] = mode
        result = self.command(self.deviceId, self._body)
        return result.text

    def set_wind_speed(self, speed: int) -> str:
        """Set fan speed

        Args:
            speed: 1-100

        Returns:
            str: result
        """
        self._body["command"] = "setWindSpeed"
        self._body["parameter"] = str(speed)
        result = self.command(self.deviceId, self._body)
        return result.text

    def set_close_delay(self, delay: int) -> str:
        """Set close delay time

        Args:
            delay: 1-36000 minutes?

        Returns:
            str: result
        """
        self._body["command"] = "closeDelay"
        self._body["parameter"] = str(delay)
        result = self.command(self.deviceId, self._body)
        return result.text
