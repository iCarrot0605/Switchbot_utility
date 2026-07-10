import json
import sys
from datetime import datetime as dt

import requests
from requests.exceptions import Timeout

from switchbot_utility.battery_mixin import BatteryMixin
from switchbot_utility.switchbot_device import SwitchbotDevice


class SwitchbotKeypad(SwitchbotDevice):
    """Switchbot Keypad class"""

    def __init__(self, deviceId):
        """Constructor"""
        super().__init__(deviceId)

    def _convert_datetime(self, datetime: str):
        """Convert datetime string to unixtime"""
        return int(dt.timestamp(dt.strptime(datetime, "%Y/%m/%d %H:%M:%S")))

    def create_key_limited(
        self,
        name: str,
        type_: str,
        password: str,
        start_time: str,
        end_time: str,
    ) -> str:
        """Create a new passcode(timiLimit or disposable)

        args:
            name: passcode name
            type: type of passcode timeLimit or disposable
            password: a 6 to 12-digit passcode in plain text
            start_time: start time like 2000/12/31 23:59:15
            end_time: end time like start_time"""
        parameter = {}
        parameter["name"] = name
        parameter["type"] = type_
        parameter["password"] = password
        parameter["startTime"] = self._convert_datetime(start_time)
        parameter["endTime"] = self._convert_datetime(end_time)

        body = {"commandType": "command", "command": "createKey"}
        body["parameter"] = parameter

        result = self.command(self.deviceId, body)
        return result.text

    def create_key(self, name: str, type_: str, password: str) -> str:
        """Create a new passcode(permanent or urgent)

        args:
            name: passcode name
            type: type of passcode permanent or urgent
            password: a 6 to 12-digit passcode in plain text"""
        parameter = {}
        parameter["name"] = name
        parameter["type"] = type_
        parameter["password"] = password

        body = {"commandType": "command", "command": "createKey"}
        body["parameter"] = parameter

        result = self.command(self.deviceId, body)
        return result.text

    def delete_key(self, keyId: str) -> str:
        body = {"commandType": "command", "command": "deleteKey"}
        parameter = {}
        parameter["id"] = keyId
        body["parameter"] = parameter

        result = self.command(self.deviceId, body)
        return result.text

    def key_list(self) -> None:
        """Get keypad key list to file"""

        header = self.gen_sign()
        try:
            response = requests.get(
                "https://api.switch-bot.com/v1.1/devices", headers=header,
                timeout=(3.0, 7.5),
            )
        except Timeout:
            sys.exit("Timeout")

        devices = json.loads(response.text)

        key_list = [
            device["keyList"]
            for device in devices["body"]["deviceList"]
            if device["deviceId"] == self.deviceId
        ]
        filename = f"keypad_{self.deviceId}_keyList.txt"
        with open(filename, "w", encoding="utf-8", newline="\n") as f:
            for key in key_list[0]:
                f.write(str(key["id"]) + ", ")
                f.write(key["name"] + ", ")
                f.write(key["type"] + ", ")
                f.write(key["status"] + "\n")
