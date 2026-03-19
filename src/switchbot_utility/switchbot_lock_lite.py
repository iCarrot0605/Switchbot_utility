from switchbot_utility.switchbot_lock import SwitchbotLock


class SwitchbotLockLite(SwitchbotLock):
    """Switchbot Lock Lite class"""

    def get_door_state(self) -> str:
        """Do Nothing, because Switchbot Lock Lite does not have a door sensor"""
        return "unknown"
