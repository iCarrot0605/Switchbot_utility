import json

import pytest

from switchbot_utility import (
    IrAirConditioner,
    SwitchbotBot,
    SwitchbotColorBulb,
    SwitchbotCurtain,
    SwitchbotKeypad,
    SwitchbotLock,
    SwitchbotMeter,
    SwitchbotPlug,
)

from conftest import make_response, sent_body

DEVICE_ID = "ABCDEF123456"


class TestBot:
    def test_turn_on(self, mock_post):
        SwitchbotBot(DEVICE_ID).turn_on()
        assert sent_body(mock_post)["command"] == "turnOn"

    def test_turn_off(self, mock_post):
        SwitchbotBot(DEVICE_ID).turn_off()
        assert sent_body(mock_post)["command"] == "turnOff"

    def test_press(self, mock_post):
        result = SwitchbotBot(DEVICE_ID).press()
        assert sent_body(mock_post)["command"] == "press"
        assert json.loads(result)["message"] == "success"

    def test_get_power_and_battery(self, status):
        status({"power": "on", "battery": 100})
        bot = SwitchbotBot(DEVICE_ID)
        assert bot.get_power() == "on"
        assert bot.get_battery() == 100


class TestCurtain:
    def test_set_position(self, mock_post):
        SwitchbotCurtain(DEVICE_ID).set_position(50)
        body = sent_body(mock_post)
        assert body["command"] == "setPosition"
        assert body["parameter"] == "0,ff,50"

    def test_open_close_are_aliases(self, mock_post):
        curtain = SwitchbotCurtain(DEVICE_ID)
        curtain.open()
        assert sent_body(mock_post)["command"] == "turnOn"
        curtain.close()
        assert sent_body(mock_post)["command"] == "turnOff"

    def test_status_getters(self, status):
        status({"slidePosition": 30, "calibrate": True, "group": False,
                "master": True})
        curtain = SwitchbotCurtain(DEVICE_ID)
        assert curtain.get_curtain_position() == 30
        assert curtain.get_calibrate() is True
        assert curtain.get_group() is False
        assert curtain.get_master() is True

    def test_parameter_does_not_leak_to_next_command(self, mock_post):
        curtain = SwitchbotCurtain(DEVICE_ID)
        curtain.set_position(50)
        curtain.turn_on()
        assert sent_body(mock_post) == {
            "commandType": "command", "parameter": "default", "command": "turnOn",
        }

    def test_parameter_does_not_leak_to_other_instance(self, mock_post):
        SwitchbotCurtain("CURTAIN_A").set_position(50)
        SwitchbotBot("BOT_B").turn_on()
        assert sent_body(mock_post)["parameter"] == "default"

    def test_body_is_reset_even_on_timeout(self, mock_post):
        from requests.exceptions import Timeout

        curtain = SwitchbotCurtain(DEVICE_ID)
        mock_post.side_effect = Timeout
        with pytest.raises(SystemExit):
            curtain.set_position(50)
        mock_post.side_effect = None
        curtain.turn_on()
        assert sent_body(mock_post)["parameter"] == "default"


class TestLock:
    @pytest.mark.parametrize("method", ["lock", "unlock", "deadbolt"])
    def test_commands(self, mock_post, method):
        getattr(SwitchbotLock(DEVICE_ID), method)()
        assert sent_body(mock_post) == {
            "commandType": "command", "parameter": "default", "command": method,
        }

    def test_status_getters(self, status):
        status({"lockState": "locked", "doorState": "closed", "battery": 60})
        lock = SwitchbotLock(DEVICE_ID)
        assert lock.get_lock_state() == "locked"
        assert lock.get_door_state() == "closed"
        assert lock.get_battery() == 60


class TestMeter:
    def test_getters(self, status):
        status({"temperature": 22.5, "humidity": 45, "battery": 100})
        meter = SwitchbotMeter(DEVICE_ID)
        assert meter.get_temperature() == 22.5
        assert meter.get_humidity() == 45
        assert meter.get_battery() == 100


class TestPlug:
    def test_turn_on(self, mock_post):
        SwitchbotPlug(DEVICE_ID).turn_on()
        assert sent_body(mock_post)["command"] == "turnOn"


class TestColorBulb:
    def test_set_color_temperature(self, mock_post):
        SwitchbotColorBulb(DEVICE_ID).set_color_temperature(4000)
        body = sent_body(mock_post)
        assert body["command"] == "setColorTemperature"
        assert body["parameter"] == 4000

    def test_get_color_temperature(self, status):
        status({"colorTemperature": 2700})
        assert SwitchbotColorBulb(DEVICE_ID).get_color_temperature() == 2700


class TestIrAirConditioner:
    def test_set_all(self, mock_post):
        IrAirConditioner(DEVICE_ID).set_all(26, 1, 3, "on")
        body = sent_body(mock_post)
        assert body["command"] == "setAll"
        assert body["parameter"] == "26, 1, 3, on"


class TestKeypad:
    def test_create_key(self, mock_post):
        SwitchbotKeypad(DEVICE_ID).create_key("guest", "permanent", "123456")
        assert sent_body(mock_post) == {
            "commandType": "command",
            "command": "createKey",
            "parameter": {"name": "guest", "type": "permanent",
                          "password": "123456"},
        }

    def test_create_key_limited_converts_datetime(self, mock_post):
        keypad = SwitchbotKeypad(DEVICE_ID)
        keypad.create_key_limited("guest", "timeLimit", "123456",
                                  "2026/01/01 00:00:00", "2026/01/02 00:00:00")
        param = sent_body(mock_post)["parameter"]
        assert param["endTime"] - param["startTime"] == 24 * 60 * 60
        assert param["startTime"] == keypad._convert_datetime("2026/01/01 00:00:00")

    def test_delete_key(self, mock_post):
        SwitchbotKeypad(DEVICE_ID).delete_key("42")
        body = sent_body(mock_post)
        assert body["command"] == "deleteKey"
        assert body["parameter"] == {"id": "42"}

    def test_key_list_writes_file(self, mock_get, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        mock_get.return_value = make_response({"body": {"deviceList": [
            {"deviceId": "OTHER", "keyList": []},
            {"deviceId": DEVICE_ID, "keyList": [
                {"id": 1, "name": "guest", "type": "permanent", "status": "normal"},
            ]},
        ]}})
        SwitchbotKeypad(DEVICE_ID).key_list()
        text = (tmp_path / f"keypad_{DEVICE_ID}_keyList.txt").read_text(encoding="utf-8")
        assert text == "1, guest, permanent, normal\n"
