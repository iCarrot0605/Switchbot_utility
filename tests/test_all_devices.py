"""Table-driven tests covering every exported device class.

Each table row is (classes, method, args, expected command, expected parameter)
for commands, or (classes, method, status body, expected value) for getters.
Subclasses that only inherit behavior are listed together with their parent so
every exported class is exercised.
"""
import inspect

import pytest

import switchbot_utility as su
from switchbot_utility.battery_mixin import BatteryMixin
from switchbot_utility.onoff_mixin import OnOffMixin

from conftest import sent_body

DEVICE_ID = "ABCDEF123456"

# ---------------------------------------------------------------- families
LOCKS = [su.SwitchbotLock, su.SwitchbotLockPro, su.SwitchbotLockUltra,
         su.SwitchbotSmartLockProWifi]
KEYPADS = [su.SwitchbotKeypad, su.SwitchbotKeypadTouch, su.SwitchbotKeypadVision,
           su.SwitchbotKeypadVisionPro]
METERS = [su.SwitchbotMeter, su.SwitchbotMeterPlus, su.SwitchbotMeterPro,
          su.SwitchbotMeterProCO2, su.SwitchbotOutdoorMeter]
CURTAINS = [su.SwitchbotCurtain, su.SwitchbotCurtain3]
HUBS = [su.SwitchbotHub2, su.SwitchbotHub3]
PLUG_MINIS = [su.SwitchbotPlugMiniUS, su.SwitchbotPlugMiniJP, su.SwitchbotPlugMiniEU]
PLUGS = [su.SwitchbotPlug] + PLUG_MINIS
AIR_PURIFIERS = [su.SwitchbotAirPurifierVOC, su.SwitchbotAirPurifierVOCTable,
                 su.SwitchbotAirPurifierPM25, su.SwitchbotAirPurifierPM25Table]
CIRCULATOR_FANS = [su.SwitchbotCirculatorFan, su.SwitchbotBatteryCirculatorFan]
EVAP_HUMIDIFIERS = [su.SwitchbotEvapolativeHumidifier,
                    su.SwitchbotEvapolativeHumidifierAutoRefill]
FLOOR_ROBOTS = [su.SwitchbotFloorCleaningRobotS10, su.SwitchbotFloorCleaningRobotS20,
                su.SwitchbotK10PlusProCombo, su.SwitchbotK11Plus,
                su.SwitchbotK20PlusPro]
VACUUMS = [su.SwitchbotRobotVacuumCleanerS1, su.SwitchbotRobotVacuumCleanerS1Plus,
           su.SwitchbotMiniRobotVacuumK10Plus, su.SwitchbotMiniRobotVacuumK10PlusPro]
MOTION_SENSORS = [su.SwitchbotMotionSensor, su.SwitchbotContactSensor]

# Strip light / bulb / ceiling light hierarchy
COLOR_LIGHTS = [su.SwitchbotStripLight, su.SwitchbotColorBulb]
CEILING_LIGHTS = [su.SwitchbotCeilingLight, su.SwitchbotCeilingLightPro]
# Inherit SwitchbotCeilingLight (whose set_color is a no-op) but override it
CEILING_DERIVED_COLOR_LIGHTS = [
    su.SwitchbotFloorLamp, su.SwitchbotStripLight3, su.SwitchbotRGBICWWStripLight,
    su.SwitchbotRGBICWWFloorLamp, su.SwitchbotRGBICNeonWireRopeLight,
    su.SwitchbotRGBICNeonWireLight,
]
ALL_LIGHTS = COLOR_LIGHTS + CEILING_LIGHTS + CEILING_DERIVED_COLOR_LIGHTS
COLOR_TEMP_LIGHTS = ALL_LIGHTS[1:]  # everything derived from SwitchbotColorBulb

IR_TVS = [su.IrTv, su.IrStreamer, su.IrSetTopBox]
IR_DVDS = [su.IrDvd, su.IrSpeaker]

EXPORTED = [obj for _, obj in inspect.getmembers(su, inspect.isclass)
            if "deviceId" in inspect.signature(obj.__init__).parameters]


def _expand(table):
    """Turn rows whose first element is a list of classes into one case per class."""
    cases = []
    for classes, *rest in table:
        for cls in classes:
            cases.append(pytest.param(cls, *rest,
                                      id=f"{cls.__name__}.{rest[0]}"))
    return cases


# ---------------------------------------------------------------- commands
COMMANDS = [
    # classes, method, args, command, parameter
    ([su.SwitchbotBot], "press", (), "press", "default"),
    (CURTAINS, "set_position", (40,), "setPosition", "0,ff,40"),
    (CURTAINS, "open", (), "turnOn", "default"),
    (CURTAINS, "close", (), "turnOff", "default"),
    ([su.SwitchbotBlindTilt], "set_position", ("up", 48), "setPosition", "up;48"),
    ([su.SwitchbotBlindTilt], "fully_open", (), "fullyOpen", "default"),
    ([su.SwitchbotBlindTilt], "close_up", (), "closeUp", "default"),
    ([su.SwitchbotBlindTilt], "close_down", (), "closeDown", "default"),
    ([su.SwitchbotRollerShade], "set_position", (30,), "setPosition", 30),
    (LOCKS + [su.SwitchbotLockLite], "lock", (), "lock", "default"),
    (LOCKS + [su.SwitchbotLockLite], "unlock", (), "unlock", "default"),
    (LOCKS, "deadbolt", (), "deadbolt", "default"),
    ([su.SwitchbotSmartLockProWifi], "night_latch_unlock", (),
     "nightLatchUnlock", "default"),
    (PLUG_MINIS, "toggle", (), "toggle", "default"),
    (AIR_PURIFIERS, "set_mode", (1, 2), "setMode", {"mode": 1, "fanGear": 2}),
    (CIRCULATOR_FANS, "set_night_light_mode", ("1",), "setNightLightMode", "1"),
    (CIRCULATOR_FANS, "set_wind_mode", ("natural",), "setWindMode", "natural"),
    (CIRCULATOR_FANS, "set_wind_speed", (50,), "setWindSpeed", "50"),
    (CIRCULATOR_FANS, "set_close_delay", (3600,), "closeDelay", "3600"),
    ([su.SwitchbotHumidifier], "set_mode", (101,), "setMode", 101),
    (EVAP_HUMIDIFIERS, "setMode", (7, 50), "setMode",
     {"mode": 7, "targetHumidity": 50}),
    (EVAP_HUMIDIFIERS, "setChildLock", (True,), "setChildLock", True),
    (FLOOR_ROBOTS, "startClean", ("sweep_mop", 2, 1, 1), "startClean",
     {"action": "sweep_mop", "fanLevel": 2, "waterLevel": 1, "times": 1}),
    (FLOOR_ROBOTS, "addWaterForHumi", (), "addWaterForHumi", "default"),
    (FLOOR_ROBOTS, "pause", (), "pause", "default"),
    (FLOOR_ROBOTS, "dock", (), "dock", "default"),
    (FLOOR_ROBOTS, "selfClean", (1,), "selfClean", 1),
    (FLOOR_ROBOTS, "setVolume", (40,), "setVolume", 40),
    (FLOOR_ROBOTS, "changeParam", (3, 2, 1), "changeParam",
     {"fanLevel": 3, "waterLevel": 2, "times": 1}),
    (VACUUMS, "start", (), "start", "default"),
    (VACUUMS, "stop", (), "stop", "default"),
    (VACUUMS, "dock", (), "dock", "default"),
    (VACUUMS, "power_level", (2,), "PowLevel", 2),
    (ALL_LIGHTS + [su.SwitchbotPermanentOutdoorLights, su.SwitchbotRGBICWWCeilingLight],
     "toggle", (), "toggle", "default"),
    (ALL_LIGHTS + [su.SwitchbotPermanentOutdoorLights], "set_brightness", (80,),
     "setBrightness", 80),
    (COLOR_LIGHTS + CEILING_DERIVED_COLOR_LIGHTS + [su.SwitchbotPermanentOutdoorLights],
     "set_color", (255, 128, 0),
     "setColor", "255:128:0"),
    (COLOR_TEMP_LIGHTS + [su.SwitchbotPermanentOutdoorLights], "set_color_temperature",
     (3000,), "setColorTemperature", 3000),
    ([su.SwitchbotRGBICWWCeilingLight], "turn_on_main_light", (),
     "turnOnMainLight", "default"),
    ([su.SwitchbotRGBICWWCeilingLight], "turn_off_main_light", (),
     "turnOffMainLight", "default"),
    ([su.SwitchbotRGBICWWCeilingLight], "turn_on_color_light", (),
     "turnOnColorLight", "default"),
    ([su.SwitchbotRGBICWWCeilingLight], "turn_off_color_light", (),
     "turnOffColorLight", "default"),
    ([su.SwitchbotRGBICWWCeilingLight], "set_main_light_brightness", (60,),
     "setMainLightBrightness", 60),
    ([su.SwitchbotRGBICWWCeilingLight], "set_main_light_color_temperature", (4000,),
     "setMainLightColorTemp", 4000),
    ([su.SwitchbotRGBICWWCeilingLight], "set_color_light_brightness", (20,),
     "setColorLightBrightness", 20),
    ([su.SwitchbotRGBICWWCeilingLight], "set_color_light_rgb", (1, 2, 3),
     "setColor", "1:2:3"),
    # IR devices
    ([su.IrAirConditioner], "set_all", (25, 2, 1, "on"), "setAll", "25, 2, 1, on"),
    (IR_TVS, "set_channel", (8,), "SetChannel", "8"),
    (IR_TVS + [su.IrSpeaker], "volume_add", (), "volumeAdd", "default"),
    (IR_TVS + [su.IrSpeaker], "volume_sub", (), "volumeSub", "default"),
    (IR_TVS, "channel_add", (), "channelAdd", "default"),
    (IR_TVS, "channel_sub", (), "channelSub", "default"),
    (IR_DVDS, "set_mute", (), "setMute", "default"),
    (IR_DVDS, "fast_forward", (), "FastForward", "default"),
    (IR_DVDS, "rewind", (), "Rewind", "default"),
    (IR_DVDS, "next_track", (), "Next", "default"),
    (IR_DVDS, "previous", (), "Previous", "default"),
    (IR_DVDS, "pause", (), "Pause", "default"),
    (IR_DVDS, "play", (), "Play", "default"),
    (IR_DVDS, "stop", (), "Stop", "default"),
    ([su.IrFan], "swing", (), "swing", "default"),
    ([su.IrFan], "timer", (), "timer", "default"),
    ([su.IrFan], "low_speed", (), "lowSpeed", "default"),
    ([su.IrFan], "middle_speed", (), "middleSpeed", "default"),
    ([su.IrFan], "high_speed", (), "highSpeed", "default"),
    ([su.IrLight], "brightness_up", (), "brightnessUp", "default"),
    ([su.IrLight], "brightness_down", (), "brightnessDown", "default"),
]


@pytest.mark.parametrize("cls, method, args, command, parameter", _expand(COMMANDS))
def test_command(mock_post, cls, method, args, command, parameter):
    device = cls(DEVICE_ID)
    result = getattr(device, method)(*args)

    assert mock_post.call_args.args[0] == (
        f"https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/commands"
    )
    assert sent_body(mock_post) == {
        "commandType": "command", "command": command, "parameter": parameter,
    }
    assert result == mock_post.return_value.text


ONOFF_CLASSES = [c for c in EXPORTED if issubclass(c, OnOffMixin)]


@pytest.mark.parametrize("cls", ONOFF_CLASSES, ids=lambda c: c.__name__)
@pytest.mark.parametrize("method, command", [("turn_on", "turnOn"),
                                             ("turn_off", "turnOff")])
def test_on_off(mock_post, cls, method, command):
    getattr(cls(DEVICE_ID), method)()
    assert sent_body(mock_post) == {
        "commandType": "command", "command": command, "parameter": "default",
    }


def test_ir_others_customize(mock_post):
    su.IrOthers(DEVICE_ID).customize("MyButton")
    assert sent_body(mock_post) == {
        "commandType": "customize", "command": "MyButton", "parameter": "default",
    }


# ---------------------------------------------------------------- no-op methods
@pytest.mark.parametrize("cls", CEILING_LIGHTS, ids=lambda c: c.__name__)
def test_ceiling_light_set_color_is_noop(mock_post, cls):
    assert cls(DEVICE_ID).set_color(1, 2, 3) is None
    mock_post.assert_not_called()


def test_lock_lite_deadbolt_is_noop(mock_post):
    assert su.SwitchbotLockLite(DEVICE_ID).deadbolt() is None
    mock_post.assert_not_called()


def test_lock_lite_door_state_is_unknown(mock_get):
    assert su.SwitchbotLockLite(DEVICE_ID).get_door_state() == "unknown"
    mock_get.assert_not_called()


# ---------------------------------------------------------------- getters
GETTERS = [
    # classes, method, status body, expected
    ([su.SwitchbotBot], "get_power", {"power": "on"}, "on"),
    (CURTAINS, "get_curtain_position", {"slidePosition": 10}, 10),
    (CURTAINS, "get_calibrate", {"calibrate": True}, True),
    (CURTAINS, "get_group", {"group": False}, False),
    (CURTAINS, "get_master", {"master": True}, True),
    ([su.SwitchbotBlindTilt], "get_direction", {"direction": "up"}, "up"),
    ([su.SwitchbotBlindTilt], "get_slide_position", {"slidePosition": 50}, 50),
    ([su.SwitchbotRollerShade], "get_calibrate", {"calibrate": True}, True),
    ([su.SwitchbotRollerShade], "get_moving", {"moving": False}, False),
    ([su.SwitchbotRollerShade], "get_slidePosition", {"slidePosition": 70}, 70),
    ([su.SwitchbotRollerShade], "get_moving", {}, None),
    (LOCKS + [su.SwitchbotLockLite], "get_lock_state", {"lockState": "locked"},
     "locked"),
    (LOCKS, "get_door_state", {"doorState": "closed"}, "closed"),
    (METERS, "get_temperature", {"temperature": 21.5}, 21.5),
    (METERS, "get_humidity", {"humidity": 40}, 40),
    ([su.SwitchbotMeterProCO2], "get_co2", {"CO2": 800}, 800),
    (HUBS, "get_temperature", {"temperature": 23.0}, 23.0),
    (HUBS, "get_humidity", {"humidity": 55}, 55),
    (HUBS, "get_light_level", {"lightLevel": 12}, 12),
    ([su.SwitchbotHub3], "get_moveDetected", {"moveDetected": True}, True),
    ([su.SwitchbotHub3], "get_onlineStatus", {"onlineStatus": "online"}, "online"),
    (MOTION_SENSORS, "get_move_detected", {"moveDetected": True}, True),
    (MOTION_SENSORS, "get_brightness", {"brightness": "bright"}, "bright"),
    ([su.SwitchbotContactSensor], "get_open_state", {"openState": "open"}, "open"),
    ([su.SwitchbotPresenceSensor], "get_lightLevel", {"lightLevel": 5}, 5),
    ([su.SwitchbotPresenceSensor], "get_detected", {"Detected": True}, True),
    ([su.SwitchbotWaterLeakDetector], "get_water_leak_state", {"status": 1}, 1),
    (PLUGS, "get_power", {"power": "off"}, "off"),
    (PLUG_MINIS, "get_voltage", {"voltage": 100.2}, 100.2),
    (PLUG_MINIS, "get_weight", {"weight": 12.5}, 12.5),
    (PLUG_MINIS, "get_electricity_of_day", {"electricityOfDay": 30}, 30),
    (PLUG_MINIS, "get_electric_current", {"electricCurrent": 0.5}, 0.5),
    (AIR_PURIFIERS, "get_power", {"power": "on"}, "on"),
    (AIR_PURIFIERS, "get_mode", {"mode": 2}, 2),
    (AIR_PURIFIERS, "get_childLock", {"childLock": 0}, 0),
    (CIRCULATOR_FANS, "get_power", {"power": "on"}, "on"),
    (CIRCULATOR_FANS, "get_mode", {"mode": "baby"}, "baby"),
    (CIRCULATOR_FANS, "get_night_status", {"nightStatus": "off"}, "off"),
    (CIRCULATOR_FANS, "get_oscillation", {"oscillation": "on"}, "on"),
    (CIRCULATOR_FANS, "get_vertical_oscillation", {"verticalOscillation": "off"},
     "off"),
    (CIRCULATOR_FANS, "get_fan_speed", {"fanSpeed": 30}, 30),
    ([su.SwitchbotBatteryCirculatorFan], "get_charging_status",
     {"chargingStatus": "charging"}, "charging"),
    ([su.SwitchbotHumidifier], "get_power", {"power": "on"}, "on"),
    ([su.SwitchbotHumidifier], "get_humidity", {"humidity": 50}, 50),
    ([su.SwitchbotHumidifier], "get_temperature", {"temperature": 20}, 20),
    ([su.SwitchbotHumidifier], "get_nebulization_efficiency",
     {"nebulizationEfficiency": 80}, 80),
    ([su.SwitchbotHumidifier], "get_auto", {"auto": True}, True),
    ([su.SwitchbotHumidifier], "get_child_lock", {"childLock": False}, False),
    ([su.SwitchbotHumidifier], "get_sound", {"sound": True}, True),
    ([su.SwitchbotHumidifier], "get_lack_water", {"lackWater": False}, False),
    (EVAP_HUMIDIFIERS, "get_power", {"power": "on"}, "on"),
    (EVAP_HUMIDIFIERS, "get_humidity", {"humidity": 45}, 45),
    (EVAP_HUMIDIFIERS, "get_mode", {"mode": 7}, 7),
    (EVAP_HUMIDIFIERS, "get_drying", {"drying": False}, False),
    (EVAP_HUMIDIFIERS, "get_childLock", {"childLock": True}, True),
    (EVAP_HUMIDIFIERS, "get_effectiveUsageHours",
     {"filterElement": {"effectiveUsageHours": 720, "usedHours": 10}}, 720),
    (EVAP_HUMIDIFIERS, "get_usedHours",
     {"filterElement": {"effectiveUsageHours": 720, "usedHours": 10}}, 10),
    (FLOOR_ROBOTS, "get_working_status", {"workingStatus": "Cleaning"}, "Cleaning"),
    (FLOOR_ROBOTS, "get_online_status", {"onlineStatus": "online"}, "online"),
    (FLOOR_ROBOTS, "get_water_base_battery", {"waterBaseBattery": 80}, 80),
    (FLOOR_ROBOTS, "get_task_type", {"taskType": "standBy"}, "standBy"),
    (VACUUMS, "get_working_status", {"workingStatus": "Clearing"}, "Clearing"),
    (VACUUMS, "get_online_status", {"onlineStatus": "offline"}, "offline"),
    (ALL_LIGHTS + [su.SwitchbotPermanentOutdoorLights], "get_power",
     {"power": "on"}, "on"),
    (ALL_LIGHTS + [su.SwitchbotPermanentOutdoorLights], "get_brightness",
     {"brightness": 70}, 70),
    (ALL_LIGHTS + [su.SwitchbotPermanentOutdoorLights], "get_color",
     {"color": "255:0:0"}, "255:0:0"),
    (COLOR_TEMP_LIGHTS + [su.SwitchbotPermanentOutdoorLights], "get_color_temperature",
     {"colorTemperature": 5000}, 5000),
    ([su.SwitchbotRGBICWWCeilingLight], "get_power", {"power": "partial"}, "partial"),
    ([su.SwitchbotRGBICWWCeilingLight], "get_online_status",
     {"onlineStatus": "online"}, "online"),
    ([su.SwitchbotRGBICWWCeilingLight], "get_main_light_power",
     {"mainLightPower": "on"}, "on"),
    ([su.SwitchbotRGBICWWCeilingLight], "get_main_light_brightness",
     {"mainLightBrightness": 90}, 90),
    ([su.SwitchbotRGBICWWCeilingLight], "get_main_light_color_temperature",
     {"mainLightColorTemp": 3000}, 3000),
    ([su.SwitchbotRGBICWWCeilingLight], "get_color_light_power",
     {"colorLightPower": "off"}, "off"),
    ([su.SwitchbotRGBICWWCeilingLight], "get_color_light_brightness",
     {"colorLightBrightness": 15}, 15),
    ([su.SwitchbotRGBICWWCeilingLight], "get_color_light_rgb",
     {"colorLightRGB": "0:0:255"}, "0:0:255"),
]


@pytest.mark.parametrize("cls, method, body, expected", _expand(GETTERS))
def test_getter(status, cls, method, body, expected):
    mock_get = status(body)
    assert getattr(cls(DEVICE_ID), method)() == expected
    assert mock_get.call_args.args[0] == (
        f"https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/status"
    )


BATTERY_CLASSES = [c for c in EXPORTED if issubclass(c, BatteryMixin)]


@pytest.mark.parametrize("cls", BATTERY_CLASSES, ids=lambda c: c.__name__)
def test_get_battery(status, cls):
    status({"battery": 60})
    assert cls(DEVICE_ID).get_battery() == 60


# ---------------------------------------------------------------- keypads
@pytest.mark.parametrize("cls", KEYPADS, ids=lambda c: c.__name__)
def test_keypad_create_and_delete_key(mock_post, cls):
    keypad = cls(DEVICE_ID)
    keypad.create_key("guest", "urgent", "654321")
    assert sent_body(mock_post)["parameter"] == {
        "name": "guest", "type": "urgent", "password": "654321",
    }
    keypad.delete_key("7")
    assert sent_body(mock_post) == {
        "commandType": "command", "command": "deleteKey", "parameter": {"id": "7"},
    }


# ---------------------------------------------------------------- coverage guard
def test_every_public_method_is_covered():
    """Fail when a new device method is added without a test in this file."""
    covered = {(cls, row[1]) for row in COMMANDS + GETTERS for cls in row[0]}
    covered |= {(c, m) for c in ONOFF_CLASSES for m in ("turn_on", "turn_off")}
    covered |= {(c, "get_battery") for c in BATTERY_CLASSES}
    covered |= {(su.IrOthers, "customize")}
    covered |= {(c, "set_color") for c in CEILING_LIGHTS}
    covered |= {(su.SwitchbotLockLite, m) for m in ("deadbolt", "get_door_state")}
    # Keypad methods are covered here and in test_devices.py
    covered |= {(c, m) for c in KEYPADS
                for m in ("create_key", "create_key_limited", "delete_key", "key_list")}

    # Methods from the base classes are tested in test_switchbot/test_device
    base = {"get_status", "command", "read_token", "gen_sign", "devicelist",
            "get_scene_list", "scene_execute"}
    missing = sorted(
        f"{cls.__name__}.{name}"
        for cls in EXPORTED
        for name, _ in inspect.getmembers(cls, inspect.isfunction)
        if not name.startswith("_") and name not in base
        and (cls, name) not in covered
    )
    assert not missing, f"untested methods: {missing}"
