class OnOffMixin:
    """On/Off devices."""

    def turn_on(self) -> str:
        """Turn on device"""
        self._body["commandType"] = "command"
        self._body["command"] = "turnOn"
        result = self.command(self.deviceId, self._body)
        return result.text

    def turn_off(self) -> str:
        """Turn off device"""
        self._body["commandType"] = "command"
        self._body["command"] = "turnOff"
        result = self.command(self.deviceId, self._body)
        return result.text
