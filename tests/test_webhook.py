import json

import pytest
from requests.exceptions import Timeout

from switchbot_utility import SwitchbotWebhook

from conftest import TOKEN, sent_body

BASE = "https://api.switch-bot.com/v1.1/webhook/"


def test_setup_webhook(mock_post):
    result = SwitchbotWebhook().setup_webhook("https://example.com/hook")
    assert mock_post.call_args.args[0] == BASE + "setupWebhook"
    assert sent_body(mock_post) == {
        "action": "setupWebhook", "deviceList": "ALL",
        "url": "https://example.com/hook",
    }
    assert json.loads(result)["message"] == "success"


def test_headers_are_sent_as_headers(mock_post):
    SwitchbotWebhook().query_url()
    kwargs = mock_post.call_args.kwargs
    assert kwargs["headers"]["Authorization"] == TOKEN
    assert "sign" in kwargs["headers"]
    assert kwargs["timeout"] == (3.0, 7.5)


def test_query_url(mock_post):
    SwitchbotWebhook().query_url()
    assert mock_post.call_args.args[0] == BASE + "queryWebhook"
    assert sent_body(mock_post) == {"action": "queryUrl"}


def test_query_details(mock_post):
    SwitchbotWebhook().query_details(["https://example.com/hook"])
    assert mock_post.call_args.args[0] == BASE + "queryWebhook"
    assert sent_body(mock_post) == {
        "action": "queryDetails", "urls": ["https://example.com/hook"],
    }


def test_update_webhook(mock_post):
    SwitchbotWebhook().update_webhook("https://example.com/hook", False)
    assert mock_post.call_args.args[0] == BASE + "updateWebhook"
    assert sent_body(mock_post) == {
        "action": "updateWebhook",
        "config": {"url": "https://example.com/hook", "enable": False},
    }


def test_delete_webhook(mock_post):
    SwitchbotWebhook().delete_webhook("https://example.com/hook")
    assert mock_post.call_args.args[0] == BASE + "deleteWebhook"
    assert sent_body(mock_post) == {
        "action": "deleteWebhook", "url": "https://example.com/hook",
    }


def test_timeout_exits(mock_post):
    mock_post.side_effect = Timeout
    with pytest.raises(SystemExit, match="Timeout"):
        SwitchbotWebhook().query_url()
