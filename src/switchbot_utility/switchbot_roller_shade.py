from switchbot_utility.switchbot_device import SwitchbotDevice
from switchbot_utility.battery_mixin import BatteryMixin


class SwitchbotRollerShade(SwitchbotDevice, BatteryMixin):
    """Switchbot Roller Shade class"""

    def get_calibrate(self) -> str:
        """determines if the open and the closed positions have been properly calibrated or not"""
        status = self.get_status()
        return status.get("calibrate")

    def get_moving(self) -> str:
        """determines if the device is moving or not"""
        status = self.get_status()
        return status.get("moving")

    def get_slidePosition(self) -> int:
        """the current position of the roller shade 0-100%

        Returns: 0-100"""
        status = self.get_status()
        return status.get("slidePosition")

    def set_position(self, position: int) -> str:
        """Set roller shade position 0-100%

        arg: position roller shade position 0-100%"""

        self._body["command"] = "setPosition"
        self._body["parameter"] = position
        result = self.command(self.deviceId, self._body)
        return result.text

