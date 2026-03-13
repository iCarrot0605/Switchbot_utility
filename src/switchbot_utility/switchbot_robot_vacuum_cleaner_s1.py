from switchbot_utility.battery_mixin import BatteryMixin
from switchbot_utility.switchbot_device import SwitchbotDevice


class SwitchbotRobotVacuumCleanerS1(SwitchbotDevice, BatteryMixin):
    """Switchbot Robot Vacuum Cleaner S1 class"""

    def __init__(self, deviceId):
        """Constructor"""
        super().__init__(deviceId)

    def start(self) -> str:
        """Start vacuuming"""
        self._body["command"] = "start"
        result = self.command(self.deviceId, self._body)
        return result.text

    def stop(self) -> str:
        """Stop vacuuming"""
        self._body["command"] = "stop"
        result = self.command(self.deviceId, self._body)
        return result.text

    def dock(self) -> str:
        """Return to charging dock"""
        self._body["command"] = "dock"
        result = self.command(self.deviceId, self._body)
        return result.text

    def power_level(self, powerlevel: int) -> str:
        """Set suction power level

        arg: 0-3"""
        self._body["command"] = "PowLevel"
        self._body["parameter"] = powerlevel
        result = self.command(self.deviceId, self._body)
        return result.text

    def get_working_status(self) -> str:
        """Returns the working status of the device"""
        status = self.get_status()
        return status["workingStatus"]

    def get_online_status(self) -> str:
        """Returns the connection status of the device"""
        status = self.get_status()
        return status["onlineStatus"]

