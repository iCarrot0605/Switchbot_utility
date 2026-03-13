class BatteryMixin:
    """Switchbot battery mixin"""
    def get_battery(self):
        """Four-segment battery level division,<10%, shown as 10;
        10%~20%, shown as 20;
        20%~60%,shown as 60;
        ≥60%, shown as 100"""
        status = self.get_status()
        return status["battery"]
