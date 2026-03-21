from switchbot_utility.switchbot_device import SwitchbotDevice
from switchbot_utility.onoff_mixin import OnOffMixin


class SwitchbotAirPurifierVOC(SwitchbotDevice, OnOffMixin):
    """Switchbot Air Purifier VOC class"""

    def get_power(self) -> str:
        """Return current state; ON, on; OFF, off

        Returns:
            str: "on" or "off"
        """
        status = self.get_status()
        return status["power"]

    def get_mode(self) -> int:
        """Return the current mode

        Returns:
            int: 1, normal or fan mode; 2, auto mode; 3, sleep mode; 4, pet mode
        """
        status = self.get_status()
        return status["mode"]

    def get_childLock(self) -> int:
        """Return if child lock is on or off

        Returns:
            int: 0 for "disabled", 1 for "enabled"
        """
        status = self.get_status()
        return status["childLock"]

    def set_mode(self, mode: int, fanLevel: int) -> str:
        """Set mode

        Args:
            mode (int): 1, normal or fan mode; 2, auto mode; 3, sleep mode; 4, pet mode
            fanLevel (int): 1-3 fan level can only be set if mode is set to 1

        Returns:
            str: result
        """
        self._body["command"] = "setMode"
        parameter = {}
        parameter["mode"] = mode
        parameter["fanGear"] = fanLevel
        self._body["parameter"] = parameter
        result = self.command(self.deviceId, self._body)
        return result.text
