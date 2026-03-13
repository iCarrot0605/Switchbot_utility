[![PyPI -
Downloads](https://img.shields.io/pypi/dm/switchbot-utility?style=plastic)](https://pypi.org/project/switchbot-utility/)
[![PyPI](https://img.shields.io/pypi/v/switchbot-utility?style=plastic)](https://pypi.org/project/switchbot-utility/)
[![PyPI -
License](https://img.shields.io/pypi/l/switchbot-utility?style=plastic)](https://pypi.org/project/switchbot-utility/)

# Switchbot_utility

Python Switchbot Utilities using Switchbot API.

## Installing

```plain
pip install switchbot-utility
```

## Getting start

Get token and secret,

1. Download the SwitchBot app on App Store or Google Play Store
2. Register a SwitchBot account and log in into your account
3. Generate an Open Token within the app
a) Go to Profile > Preference
b) Tap App Version 10 times. Developer Options will show up
c) Tap Developer Options
d) Copy token and secret

create `settings.json` file, and fill token and secret.

```python
{
    "token": "",
    "secret": ""
}
```

Run example script.

```python
import switchbot_utility.switchbot as sbu

switchbot = sbu.Switchbot()
switchbot.devicelist()
```

Scripts makes `deviceList.txt`. You can manipulate device using diviceId in this file.

## Other Example

### Get temperature from SwitchbotMeter

```python
import switchbot_utility as sbu

meter = sbu.SwitchbotMeter("meterDeviceId")
print(meter.get_temperature())
```

### Unlock SwitchbotLock

```python
import switchbot_utility as sbu

lock = sbu.SwitchbotLock("lockDeviceId")
lock.unlock()
```

## Commands reference

[Read the document](https://icarrot0605.github.io/switchbot_utility_docs/)

## Supported device

| Term                         | Description                                                  |Tested |
| ---------------------------- | ------------------------------------------------------------ | ------ |
| Hub                          | Generally referred to these devices, SwitchBot Hub Model No. SwitchBot Hub S1/SwitchBot Hub Mini Model No. W0202200/SwitchBot Hub Plus Model No. SwitchBot Hub S1 | No |
| Hub Mini                     | Short for SwitchBot Hub Mini Model No. W0202200              | Yes |
| Hub Plus                     | Short for SwitchBot Hub Plus Model No. SwitchBot Hub S1      | No |
| Hub 2                     | Short for SwitchBot Hub 2 Model No. W3202100      | Yes |
| Bot                          | Short for SwitchBot Bot Model No. SwitchBot S1               | Yes |
| Curtain                      | Short for SwitchBot Curtain Model No. W0701600               | Yes |
| Plug                         | Short for SwitchBot Plug Model No. SP11. Currently only available in Japan | Yes |
| Meter                        | Short for SwitchBot Thermometer and Hygrometer Model No. SwitchBot MeterTH S1 | Yes |
| Meter Plus (JP)              | Short for SwitchBot Thermometer and Hygrometer Plus (JP) Model No. W2201500 | Yes |
| Meter Plus (US)              | Short for SwitchBot Thermometer and Hygrometer Plus (US) Model No. W2301500 | No |
| Outdoor Meter                | Short for Indoor/Outdoor Thermo-Hygrometer Model No. W3400010 | Yes |
| Meter Pro                    | Short for SwitchBot Meter Pro Model No. W4900000              | No |
| Meter Pro (CO2 Monitor)      | Short for SwitchBot Meter Pro (CO2 Monitor) Model No. W4900010 | Yes |
| Motion Sensor                | Short for SwitchBot Motion Sensor Model No. W1101500         | No |
| Contact Sensor               | Short for SwitchBot Contact Sensor Model No. W1201500        | Yes |
| Water Leak Detector          | Short for SwitchBot Water Leak Detector Model No. W4402000    | Yes |
| Color Bulb                   | Short for SwitchBot Color Bulb Model No. W1401400            | Yes |
| Strip Light                  | Short for SwitchBot LED Strip Light Model No. W1701100       | No |
| Plug Mini (US)               | Short for SwitchBot Plug Mini (US) Model No. W1901400 and W1901401 | No |
| Plug Mini (EU)               | Short for SwitchBot Plug Mini (EU) Model No. W7732300 | No |
| Plug Mini (JP)               | Short for SwitchBot Plug Mini (JP) Model No. W2001400 and W2001401 | Yes |
| Lock                         | Short for SwitchBot Lock Model No. W1601700                  | Yes |
| Keypad                         | Short for SwitchBot Lock Model No. W2500010                  | No |
| Keypad Touch                         | Short for SwitchBot Lock Model No. W2500020                  | Yes |
| Robot Vacuum Cleaner S1      | Short for SwitchBot Robot Vacuum Cleaner S1 Model No. W3011000. Currently only available in Japan. | No |
| Robot Vacuum Cleaner S1 Plus | Short for SwitchBot Robot Vacuum Cleaner S1 Plus Model No. W3011010. Currently only available in Japan. | No |
| K10+                         | Short for SwitchBot Mini Robot Vacuum K10+ Model No. W3011020 | Yes |
| K10+ Pro                     | Short for SwitchBot Mini Robot Vacuum K10+ Pro Model No. W3011026 | No |
| S10                          | Short for SwitchBot Floor Cleaning Robot S10 Model No. W3211800   | No |
| S20                          | Short for SwitchBot Floor Cleaning Robot S20 Model No. W6602310   | No |
| K10+ Pro Combo               | Short for SwitchBot Robot Vacuum K10+ Pro Combo Model No. W3002500 | No |
| K20+ Pro                     | Short for SwitchBot Multitasking Household Robot K20+ Pro Model No. W3002520 | No |
| K11+                         | Short for Robot Vacuum K11+ Model No. W3003100 | No |
| Ceiling Light      | Short for SwitchBot Ceiling Light Model No. W2612230 and W2612240. Currently only available in Japan. | No |
| Ceiling Light Pro | Short for SwitchBot Ceiling Light Pro Model No. W2612210 and W2612220. Currently only available in Japan. | No |
| Indoor Cam | Short for SwitchBot Indoor Cam Model No. W1301200                  | No |
| Pan/Tilt Cam | Short for SwitchBot Pan/Tilt Cam Model No. W1801200                  | No |
| Pan/Tilt Cam 2K | Short for SwitchBot Pan/Tilt Cam 2K Model No. W3101100                  | No |
| Blind Tilt | Short for SwitchBot Blind Tilt Model No. W2701600 | No |
