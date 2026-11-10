from switchbot_utility.switchbot_hub2 import SwitchbotHub2


class SwitchbotHub3(SwitchbotHub2):
    """Switchbot Hub3 class"""

    def get_moveDetected(self) -> bool:
        """determines if motion is detected

        Returns:
            bool: True if motion is detected, False otherwise
        """
        status = self.get_status()
        return status["moveDetected"]

    def get_onlineStatus(self) -> str:
        """the connection status of the device.

        Returns:
            online or offline
        """
        status = self.get_status()
        return status["onlineStatus"]
