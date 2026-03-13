from switchbot_utility.switchbot_device import SwitchbotDevice
from switchbot_utility.battery_mixin import BatteryMixin


class SwitchbotFloorCleaningRobotS10(SwitchbotDevice, BatteryMixin):
    """Switchbot Floor Cleaning Robot S10 class"""

    def get_working_status(self) -> str:
        """Get current working status

        Returns:
            str: Current working status
        """
        status = self.get_status()
        return status["workingStatus"]

    def get_online_status(self) -> str:
        """Get current online status

        Returns:
            str: Current online status
        """
        status = self.get_status()
        return status["onlineStatus"]

    def get_water_base_battery(self) -> int:
        """Get water base battery level

        Returns:
            int: Water base battery level
        """
        status = self.get_status()
        return status["waterBaseBattery"]

    def get_task_type(self) -> str:
        """Get current task type

        Returns:
            str: Current task type
        """
        status = self.get_status()
        return status["taskType"]

    def startClean(self, action: str, fanLevel: int, waterLevel: int, times: int) -> str:
        """Start cleaning

        Args:
            action (str): cleaning mode, sweep or sweep_mop
            fanLevel (int): Vacuum level (1-4)
            waterLevel (int): Mop moisture level (1-2)
            times (int): Number of cleaning cycles (1-2639999)

        Returns:
            str: Result of the command
        """
        self._body["command"] = "startClean"
        parameter = {}
        parameter["action"] = action
        parameter["fanLevel"] = fanLevel
        parameter["waterLevel"] = waterLevel
        parameter["times"] = times
        self._body["parameter"] = parameter
        result = self.command(self.deviceId, self._body)
        return result.text

    def addWaterForHumi(self) -> str:
        """Refill the mind blowing Evaporative Humidifier (Auto-refill).

        Returns:
            str: Result of the command
        """
        self._body["command"] = "addWaterForHumi"
        result = self.command(self.deviceId, self._body)
        return result.text

    def pause(self) -> str:
        """Pause cleaning

        Returns:
            str: Result of the command
        """
        self._body["command"] = "pause"
        result = self.command(self.deviceId, self._body)
        return result.text

    def dock(self) -> str:
        """Return to Auto-empty Station and charge.

        Returns:
            str: Result of the command
        """
        self._body["command"] = "dock"
        result = self.command(self.deviceId, self._body)
        return result.text

    def setVolume(self, volume: int) -> str:
        """Set the volume (1-100)

        Args:
            volume (int): Volume level (0-100)

        Returns:
            str: Result of the command
        """
        self._body["command"] = "setVolume"
        parameter = {}
        parameter["volume"] = volume
        self._body["parameter"] = parameter
        result = self.command(self.deviceId, self._body)
        return result.text

    def selfClean(self, mode: int) -> str:
        """Start self-cleaning

        Args:
            mode 1, wash the mop.
            mode 2, dry itself.
            mode 3, terminate

        Returns:
            str: Result of the command
        """
        self._body["command"] = "selfClean"
        parameter = {}
        parameter["mode"] = mode
        self._body["parameter"] = parameter
        result = self.command(self.deviceId, self._body)
        return result.text

    def changeParam(self, fanLevel: int, waterLevel: int, times: int) -> str:
        """Change the fan level and water level during cleaning

        Args:
            fanLevel (int): Vacuum level (1-4)
            waterLevel (int): Mop moisture level (1-2)
            times (int): Number of cleaning cycles (1-2639999)

        Returns:
            str: Result of the command
        """
        self._body["command"] = "changeParam"
        parameter = {}
        parameter["fanLevel"] = fanLevel
        parameter["waterLevel"] = waterLevel
        parameter["times"] = times
        self._body["parameter"] = parameter
        result = self.command(self.deviceId, self._body)
        return result.text
