from switchbot_utility.onoff_mixin import OnOffMixin
from switchbot_utility.switchbot_device import SwitchbotDevice


class SwitchbotBlindTilt(SwitchbotDevice, OnOffMixin):
    """Switchbot Blind Tilt class"""

    def set_position(self, direction: str, position: int) -> str:
        """Set blind position.

        Args:
            direction (str): up/down
            position (int): 0~100 (0 means closed,
            100 means open, it MUST be set to a multiple of 2.
            for example, up;48 or up; 36)

        Returns:
            str: result
        """

        self._body["command"] = "setPosition"
        self._body["parameter"] = "{};{}".format(direction, position)
        result = self.command(self.deviceId, self._body)
        return result.text

    def fully_open(self) -> str:
        """Set the position of Blind Tilt to open.

        Returns:
            str: result
        """
        self._body["command"] = "fullyOpen"
        self._body["parameter"] = "default"
        result = self.command(self.deviceId, self._body)
        return result.text

    def close_up(self) -> str:
        """Set the position of Blind Tilt to closed up.

        Returns:
            str: result
        """
        self._body["command"] = "closeUp"
        self._body["parameter"] = "default"
        result = self.command(self.deviceId, self._body)
        return result.text

    def close_down(self) -> str:
        """Set the position of Blind Tilt to closed down.

        Returns:
            str: result
        """
        self._body["command"] = "closeDown"
        self._body["parameter"] = "default"
        result = self.command(self.deviceId, self._body)
        return result.text

    def get_direction(self) -> str:
        """Return the opening direction of a Blind Tilt device

        Returns:
            str: result
        """
        status = self.get_status()
        return status["direction"]

    def get_slide_position(self) -> int:
        """Return the current position, 0-100.

        Returns:
            int: current position
        """
        status = self.get_status()
        return status["slidePosition"]
