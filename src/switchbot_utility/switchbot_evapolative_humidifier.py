from switchbot_utility.switchbot_device import SwitchbotDevice
from switchbot_utility.onoff_mixin import OnOffMixin


class SwitchbotEvapolativeHumidifier(SwitchbotDevice, OnOffMixin):
    """SwitchBot Evapolative Humidifier."""

    def get_power(self) -> str:
        """Get power status."""
        status = self.get_status()
        return status["power"]

    def get_humidity(self) -> int:
        """Get humidity."""
        status = self.get_status()
        return status["humidity"]

    def get_mode(self) -> int:
        """Get mode.

        1: Level4
        2: Level3
        3: Level2
        4: Level1
        5: humidity mode
        6: sleep mode
        7: auto mode
        8: drying mode"""
        status = self.get_status()
        return status["mode"]

    def get_drying(self) -> bool:
        """Get drying status."""
        status = self.get_status()
        return status["drying"]

    def get_childLock(self) -> bool:
        """Get child lock status."""
        status = self.get_status()
        return status["childLock"]

    def get_effectiveUsageHours(self) -> int:
        """Get effective usage hours."""
        status = self.get_status()
        return status["filterElement"]["effectiveUsageHours"]

    def get_usedHours(self) -> int:
        """Get used hours."""
        status = self.get_status()
        return status["filterElement"]["usedHours"]

    def setMode(self, mode: int, targetHumidity: int) -> str:
        """Set mode.

        Args:
            mode (int): Mode to set
            1: Level4
            2: Level3
            3: Level2
            4: Level1
            5: humidity mode
            6: sleep mode
            7: auto mode
            8: drying mode
            targetHumidity (int): Target humidity (0-100)

        Returns:
            str: Result of the command
        """
        self._body["command"] = "setMode"
        parameter = {}
        parameter["mode"] = mode
        parameter["targetHumidity"] = targetHumidity
        self._body["parameter"] = parameter
        result = self.command(self.deviceId, self._body)
        return result.text

    def setChildLock(self, lock: bool) -> str:
        """Set child lock.

        Args:
            lock (bool): True to lock, False to unlock

        Returns:
            str: Result of the command
        """
        self._body["command"] = "setChildLock"
        self._body["parameter"] = lock
        result = self.command(self.deviceId, self._body)
        return result.text
