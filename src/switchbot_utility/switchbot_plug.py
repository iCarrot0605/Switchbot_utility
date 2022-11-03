from .switchbot_device import SwitchbotDevice
from .onoff_ability import OnOffAbirity


class SwitchbotPlug(SwitchbotDevice, OnOffAbirity):
    """Switchbot Plug class"""
    def __init__(self, deviceId):
        """Constructor"""
        super().__init__(deviceId)

    def get_power(self):
        """Returns device power status"""
        status = self.get_status()
        return status['power']