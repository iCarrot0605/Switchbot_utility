from switchbot_utility.battery_mixin import BatteryMixin
from switchbot_utility.onoff_mixin import OnOffMixin
from switchbot_utility.switchbot_device import SwitchbotDevice


class SwitchbotCurtain(SwitchbotDevice, OnOffMixin, BatteryMixin):
    """Switchbot Curtain class"""

    def set_position(self, position: int) -> str:
        """Set curtain position 0-100%

        arg: position curtain position 0-100%"""

        self._body["command"] = "setPosition"
        self._body["parameter"] = "0,ff,{}".format(position)
        result = self.command(self.deviceId, self._body)
        return result.text

    def open(self) -> str:
        """Aliase of turn on command"""
        return self.turn_on()

    def close(self) -> str:
        """Aliase of turn off command"""
        return self.turn_off()

    def get_curtain_position(self) -> dict:
        """Returns curtain position 0(open) to 100(close)"""
        status = self.get_status()
        return status["slidePosition"]

    def get_calibrate(self) -> bool:
        """determines if the open position and the close position of
        a device have been properly calibrated or not

        Returns:
            bool: True if the device has been calibrated, False otherwise
        """
        status = self.get_status()
        return status["calibrate"]

    def get_group(self) -> bool:
        """determines if a Curtain is paired with or grouped
        with another Curtain or not

        Returns:
            bool: True if the device is part of a group, False otherwise
        """
        status = self.get_status()
        return status["group"]

    def get_master(self) -> bool:
        """determines if a Curtain is the master device or not when
        paired with or grouped with another Curtain

        Returns:
            bool: True if the device is the master device in a group, False otherwise
        """
        status = self.get_status()
        return status["master"]

