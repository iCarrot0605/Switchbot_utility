import json
import sys

import requests
from requests.exceptions import Timeout

from switchbot_utility.command_mixin import CommandMixin
from switchbot_utility.switchbot import Switchbot


class SwitchbotDevice(Switchbot, CommandMixin):
    """Switchbot device class"""

    _baseurl = "https://api.switch-bot.com/v1.1/devices/"

    def __init__(self, deviceId):
        """Constructor"""
        self.deviceId = deviceId

    def get_status(self) -> dict:
        """Get device information"""
        header = self.gen_sign()
        try:
            response = requests.get(
                self._baseurl + self.deviceId + "/status",
                headers=header, timeout=(3.0, 7.5)
            )
        except Timeout:
            sys.exit("Timeout")

        status = json.loads(response.text)
        if status["message"] != "success":
            sys.exit(status["message"])
        else:
            return status["body"]
