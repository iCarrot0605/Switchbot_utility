from switchbot_utility.switchbot_lock import SwitchbotLock


class SwitchbotSmartLockProWifi(SwitchbotLock):
    """Switchbot Smart Lock Pro Wifi class"""

    def night_latch_unlock(self) -> str:
        """Unlock the night latch(EU)"""
        body = {
            "commandType": "command",
            "parameter": "default",
            "command": "nightLatchUnlock",
        }
        result = self.command(self.deviceId, body)
        return result.text
