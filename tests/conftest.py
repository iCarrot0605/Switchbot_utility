import json
from unittest.mock import MagicMock

import pytest

from switchbot_utility.switchbot import Switchbot

TOKEN = "test-token"
SECRET = "test-secret"


def make_response(payload):
    """Build a fake requests.Response-like object."""
    response = MagicMock()
    response.text = json.dumps(payload) if not isinstance(payload, str) else payload
    return response


@pytest.fixture(autouse=True)
def fake_token(monkeypatch):
    """Never read the real settings.json during tests."""
    monkeypatch.setattr(Switchbot, "read_token", lambda self: (TOKEN, SECRET))


@pytest.fixture
def mock_post(monkeypatch):
    """Patch requests.post and return the mock; default response is success."""
    mock = MagicMock(return_value=make_response({"statusCode": 100, "message": "success"}))
    monkeypatch.setattr("requests.post", mock)
    return mock


@pytest.fixture
def mock_get(monkeypatch):
    """Patch requests.get; set mock.return_value = make_response(...) in tests."""
    mock = MagicMock()
    monkeypatch.setattr("requests.get", mock)
    return mock


@pytest.fixture
def status(mock_get):
    """Helper: status({...}) makes get_status() return the given body."""

    def _set(body):
        mock_get.return_value = make_response(
            {"statusCode": 100, "message": "success", "body": body}
        )
        return mock_get

    return _set


def sent_body(mock_post):
    """Return the JSON body of the last requests.post call."""
    return json.loads(mock_post.call_args.kwargs["data"])
