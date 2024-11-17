from command_mixin import CommandMixin
from onoff_mixin import OnOffMixin
from switchbot import Switchbot


class SwitchbotIrDevice(Switchbot, OnOffMixin, CommandMixin):
    """Switchbot virtual ir device"""

    def __init__(self, deviceId):
        """Constructor"""
        self.deviceId = deviceId
