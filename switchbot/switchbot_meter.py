from .switchbot_device import SwitchbotDevice

class SwitchbotMeter(SwitchbotDevice):
    """Switchbot meter class"""
    def __init__(self, deviceId):
        """Constructor"""
        super().__init__(deviceId)

    def get_temperature(self):
        """Returns temperature form meter"""
        status = self.get_status()
        return status['temperature']

    def get_humidity(self):
        """Returns temperature form meter"""
        status = self.get_status()
        return status['humidity']