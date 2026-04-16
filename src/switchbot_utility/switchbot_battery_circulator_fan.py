from switchbot_utility.switchbot_circulator_fan import SwitchbotCirculatorFan
from switchbot_utility.battery_mixin import BatteryMixin


class SwitchbotBatteryCirculatorFan(SwitchbotCirculatorFan, BatteryMixin):
    """Switchbot Battery Circulator Fan class"""

    def get_charging_status(self) -> str:
        """Get charge status

        Returns:
            str: charging or uncharged
        """
        status = self.get_status()
        return status["chargingStatus"]
