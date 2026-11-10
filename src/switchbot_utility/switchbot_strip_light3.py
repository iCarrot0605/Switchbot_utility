from switchbot_utility.switchbot_ceiling_light import SwitchbotCeilingLight
from switchbot_utility.switchbot_strip_light import SwitchbotStripLight


class SwitchbotStripLight3(SwitchbotCeilingLight):
    """Switchbot Strip Light 3 class"""

    # SwitchbotCeilingLight.set_color is a no-op; this device supports color
    set_color = SwitchbotStripLight.set_color

