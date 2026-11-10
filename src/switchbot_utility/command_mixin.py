import json
import sys

import requests
from requests.exceptions import Timeout


class CommandMixin:
    _DEFAULT_BODY = {"commandType": "command", "parameter": "default"}
    _baseurl = "https://api.switch-bot.com/v1.1/devices/"

    @property
    def _body(self) -> dict:
        """Per-instance command body, reset to defaults after every command.

        Kept per instance (not shared on the class) so that a parameter set
        by one command never leaks into the next command or another device.
        """
        if "_command_body" not in self.__dict__:
            self._command_body = dict(self._DEFAULT_BODY)
        return self._command_body

    def command(self, deviceId: str, body: dict):
        """Send command"""

        header = self.gen_sign()
        try:
            return requests.post(
                self._baseurl + deviceId + "/commands",
                headers=header,
                data=json.dumps(body),
                timeout=(3.0, 7.5)
            )
        except Timeout:
            sys.exit("Timeout")
        finally:
            self.__dict__.pop("_command_body", None)
