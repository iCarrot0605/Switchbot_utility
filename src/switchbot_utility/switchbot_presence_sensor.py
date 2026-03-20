from switchbot_utility.switchbot_device import SwitchbotDevice
from switchbot_utility.battery_mixin import BatteryMixin


class SwitchbotPresenceSensor(SwitchbotDevice, BatteryMixin):
    def get_lightLevel(self) -> int:
        """ Returns the level of illuminance of the ambience light

        Returns: 1-20"""
        status = self.get_status()
        return status["lightLevel"]

    def get_detected(self) -> bool:
        """ determines if human is detected

        Returns: True/False"""
        status = self.get_status()
        return status["Detected"]

