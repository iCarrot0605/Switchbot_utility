from switchbot_utility.battery_mixin import BatteryMixin
from switchbot_utility.switchbot_device import SwitchbotDevice

class SwitchbotWaterLeakDetector(BatteryMixin, SwitchbotDevice):
    """Switchbot Water Leak Detector class"""

    def get_water_leak_state(self) -> dict:
        """Returns the water leak state of the sensor"""
        status = self.get_status()
        return status["status"]
