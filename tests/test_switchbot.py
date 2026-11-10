import base64
import hashlib
import hmac
import json

import pytest
from requests.exceptions import Timeout

from switchbot_utility.switchbot import Switchbot

from conftest import SECRET, TOKEN, make_response


class TestReadToken:
    @pytest.fixture(autouse=True)
    def restore_read_token(self, monkeypatch, tmp_path):
        # undo the autouse fake so the real implementation is tested
        monkeypatch.undo()
        monkeypatch.chdir(tmp_path)

    def test_reads_settings(self, tmp_path):
        (tmp_path / "settings.json").write_text(
            json.dumps({"token": "abc", "secret": "xyz"}), encoding="utf8"
        )
        assert Switchbot().read_token() == ("abc", "xyz")

    def test_missing_file_exits(self):
        with pytest.raises(SystemExit, match="does not exist"):
            Switchbot().read_token()

    def test_missing_key_exits(self, tmp_path):
        (tmp_path / "settings.json").write_text(json.dumps({"token": "abc"}))
        with pytest.raises(SystemExit, match="invarid"):
            Switchbot().read_token()


class TestGenSign:
    def test_header_fields(self):
        header = Switchbot().gen_sign()
        assert header["Authorization"] == TOKEN
        assert header["Content-Type"] == "application/json; charset=utf8"
        assert set(header) == {"Content-Type", "Authorization", "sign", "t", "nonce"}

    def test_signature_is_valid_hmac(self):
        header = Switchbot().gen_sign()
        msg = f"{TOKEN}{header['t']}{header['nonce']}".encode()
        expected = base64.b64encode(
            hmac.new(SECRET.encode(), msg, hashlib.sha256).digest()
        ).decode()
        assert header["sign"] == expected

    def test_nonce_is_unique(self):
        assert Switchbot().gen_sign()["nonce"] != Switchbot().gen_sign()["nonce"]


class TestDeviceList:
    def test_writes_device_list(self, mock_get, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        mock_get.return_value = make_response({
            "message": "success",
            "body": {
                "deviceList": [
                    {"deviceId": "A1", "deviceName": "Bot", "deviceType": "Bot",
                     "hubDeviceId": "H1"},
                    {"deviceId": "A2", "deviceName": "Hub"},  # missing keys
                ],
                "infraredRemoteList": [
                    {"deviceId": "IR1", "deviceName": "TV", "remoteType": "TV",
                     "hubDeviceId": "H1"},
                ],
            },
        })
        Switchbot().devicelist()

        lines = (tmp_path / "deviceList.txt").read_text(encoding="utf-8").splitlines()
        assert lines == [
            "A1, Bot, Bot, H1",
            "A2, Hub, , ",
            "IR1, TV, TV, H1",
        ]
        assert mock_get.call_args.args[0] == "https://api.switch-bot.com/v1.1/devices"

    def test_timeout_exits(self, mock_get):
        mock_get.side_effect = Timeout
        with pytest.raises(SystemExit, match="Timeout"):
            Switchbot().devicelist()


class TestScene:
    def test_get_scene_list(self, mock_get, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        mock_get.return_value = make_response({
            "message": "success",
            "body": [{"sceneId": "S1", "sceneName": "Morning"},
                     {"sceneId": "S2", "sceneName": "Night"}],
        })
        Switchbot().get_scene_list()
        text = (tmp_path / "sceneList.txt").read_text(encoding="utf-8")
        assert text == "S1, Morning\nS2, Night\n"

    def test_get_scene_list_error_exits(self, mock_get, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        mock_get.return_value = make_response({"message": "Unauthorized"})
        with pytest.raises(SystemExit, match="Unauthorized"):
            Switchbot().get_scene_list()

    def test_scene_execute(self, mock_post):
        result = Switchbot().scene_execute("S1")
        assert mock_post.call_args.kwargs["url"] == (
            "https://api.switch-bot.com/v1.1/scenes/S1/execute"
        )
        assert json.loads(result)["message"] == "success"
