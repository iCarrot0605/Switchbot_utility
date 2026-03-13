import base64
import hashlib
import hmac
import json
import sys
import time
import uuid

import requests
from requests.exceptions import Timeout


class Switchbot:
    """Switchbot Utility class"""

    def __init__(self):
        """Constructor"""

    def read_token(self) -> tuple:
        """Import access token and secret from settings.json"""
        try:
            with open("settings.json", "r", encoding="utf8") as f:
                settings = json.load(f)
            token = settings["token"]
            secret = settings["secret"]
            return token, secret
        except FileNotFoundError:
            sys.exit("settings.json file does not exist")
        except KeyError:
            sys.exit("settings.json file is invarid")

    def gen_sign(self) -> dict:
        """Generate Switchbot API v1.1 sign header

        Returns:
        Switchbot API v1.1 sign header
        """

        token, secret = self.read_token()

        nonce = str(uuid.uuid4())
        t = int(round(time.time() * 1000))
        string_to_sign = "{}{}{}".format(token, t, nonce)

        string_to_sign = bytes(string_to_sign, "utf-8")
        secret = bytes(secret, "utf-8")

        hmacstr = hmac.new(
            secret, msg=string_to_sign, digestmod=hashlib.sha256
        ).digest()
        sign = base64.b64encode(hmacstr)

        header = {}
        header["Content-Type"] = "application/json; charset=utf8"
        header["Authorization"] = token
        header["sign"] = str(sign, "utf-8")
        header["t"] = str(t)
        header["nonce"] = nonce

        return header

    def devicelist(self) -> None:
        """Create all Switchbot device list as deviceList.txt"""
        header = self.gen_sign()
        try:
            response = requests.get(
                "https://api.switch-bot.com/v1.1/devices", headers=header,
                timeout=(3.0, 7.5)
            )
        except Timeout:
            sys.exit("Timeout")

        devices = json.loads(response.text)

        with open("deviceList.txt", "w", encoding="utf-8", newline="\n") as f:
            for device in devices["body"]["deviceList"]:
                try:
                    f.write(device["deviceId"] + ", ")
                except KeyError:
                    f.write(", ")
                try:
                    f.write(device["deviceName"] + ", ")
                except KeyError:
                    f.write(", ")
                try:
                    f.write(device["deviceType"] + ", ")
                except KeyError:
                    f.write(", ")
                try:
                    f.write(device["hubDeviceId"] + "\n")
                except KeyError:
                    f.write("\n")

            for device in devices["body"]["infraredRemoteList"]:
                try:
                    f.write(device["deviceId"] + ", ")
                except KeyError:
                    f.write(", ")
                try:
                    f.write(device["deviceName"] + ", ")
                except KeyError:
                    f.write(", ")
                try:
                    f.write(device["remoteType"] + ", ")
                except KeyError:
                    f.write(", ")
                try:
                    f.write(device["hubDeviceId"] + "\n")
                except KeyError:
                    f.write("\n")

    def get_scene_list(self) -> None:
        """Get scene List as sceneList.txt"""
        header = self.gen_sign()
        try:
            response = requests.get(
                "https://api.switch-bot.com/v1.1/scenes", headers=header,
                timeout=(3.0, 7.5),
            )
        except Timeout:
            sys.exit("Timeout")

        scenes = json.loads(response.text)

        if scenes["message"] != "success":
            sys.exit(scenes["message"])
        else:
            with open(
                "sceneList.txt", "w", encoding="utf-8", newline="\n"
            ) as f:
                for scene in scenes["body"]:
                    f.write(scene["sceneId"] + ", ")
                    f.write(scene["sceneName"] + "\n")

    def scene_execute(self, sceneId: str) -> str:
        """Execute scene"""
        header = self.gen_sign()
        url = "https://api.switch-bot.com/v1.1/scenes/" + sceneId + "/execute"
        try:
            response = requests.post(url=url, headers=header,
                                     timeout=(3.0, 7.5))
        except Timeout:
            sys.exit("Timeout")

        return response.text
