from switchbot_utility.battery_mixin import BatteryMixin
from switchbot_utility.switchbot_device import SwitchbotDevice


class SwitchbotLock(SwitchbotDevice, BatteryMixin):
    """Switchbot Lock class"""

    def lock(self) -> str:
        """Lock a lock"""
        body = {
            "commandType": "command",
            "parameter": "default",
            "command": "lock",
        }
        result = self.command(self.deviceId, body)
        return result.text

    def unlock(self) -> str:
        """Unlock a lock"""
        body = {
            "commandType": "command",
            "parameter": "default",
            "command": "unlock",
        }
        result = self.command(self.deviceId, body)
        return result.text

    def deadbolt(self) -> str:
        """Disengage deadbolt or latch"""
        body = {
            "commandType": "command",
            "parameter": "default",
            "command": "deadbolt",
        }
        result = self.command(self.deviceId, body)
        return result.text

    def get_lock_state(self) -> str:
        """Returns if locked or not"""
        status = self.get_status()
        return status["lockState"]

    def get_door_state(self) -> str:
        """Returns if closed or not"""
        status = self.get_status()
        return status["doorState"]
