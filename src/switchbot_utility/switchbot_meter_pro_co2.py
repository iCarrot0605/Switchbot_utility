from switchbot_utility.switchbot_meter import SwitchbotMeter


class SwitchbotMeterProCO2(SwitchbotMeter):
    """Switchbot Meter Pro CO2 class"""

    def get_co2(self) -> dict:
        """Returns the CO2 level of the sensor"""
        status = self.get_status()
        return status["CO2"]
