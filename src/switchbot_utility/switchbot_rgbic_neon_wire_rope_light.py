from switchbot_utility.switchbot_ceiling_light import SwitchbotCeilingLight
from switchbot_utility.switchbot_strip_light import SwitchbotStripLight


class SwitchbotRGBICNeonWireRopeLight(SwitchbotCeilingLight):
    """Switchbot RGBIC Neon Wire Rope Light class"""

    # SwitchbotCeilingLight.set_color is a no-op; this device supports color
    set_color = SwitchbotStripLight.set_color

