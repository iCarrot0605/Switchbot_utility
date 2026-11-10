import inspect

import pytest
from requests.exceptions import Timeout

import switchbot_utility
from switchbot_utility.switchbot_device import SwitchbotDevice

from conftest import make_response, sent_body

DEVICE_ID = "ABCDEF123456"


class TestGetStatus:
    def test_success_returns_body(self, status):
        mock_get = status({"power": "on"})
        assert SwitchbotDevice(DEVICE_ID).get_status() == {"power": "on"}
        assert mock_get.call_args.args[0] == (
            f"https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/status"
        )
        assert "sign" in mock_get.call_args.kwargs["headers"]

    def test_error_message_exits(self, mock_get):
        mock_get.return_value = make_response({"message": "device not found"})
        with pytest.raises(SystemExit, match="device not found"):
            SwitchbotDevice(DEVICE_ID).get_status()

    def test_timeout_exits(self, mock_get):
        mock_get.side_effect = Timeout
        with pytest.raises(SystemExit, match="Timeout"):
            SwitchbotDevice(DEVICE_ID).get_status()


class TestCommand:
    def test_posts_to_commands_endpoint(self, mock_post):
        body = {"commandType": "command", "command": "turnOn", "parameter": "default"}
        SwitchbotDevice(DEVICE_ID).command(DEVICE_ID, body)

        assert mock_post.call_args.args[0] == (
            f"https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/commands"
        )
        assert sent_body(mock_post) == body
        assert mock_post.call_args.kwargs["timeout"] == (3.0, 7.5)

    def test_timeout_exits(self, mock_post):
        mock_post.side_effect = Timeout
        with pytest.raises(SystemExit, match="Timeout"):
            SwitchbotDevice(DEVICE_ID).command(DEVICE_ID, {})


def _exported_device_classes():
    return [
        obj for _, obj in inspect.getmembers(switchbot_utility, inspect.isclass)
        if "deviceId" in inspect.signature(obj.__init__).parameters
    ]


@pytest.mark.parametrize("cls", _exported_device_classes(), ids=lambda c: c.__name__)
def test_every_device_class_can_be_instantiated(cls):
    device = cls(DEVICE_ID)
    assert device.deviceId == DEVICE_ID
    assert callable(device.command)
