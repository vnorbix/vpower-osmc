import time
import traceback
import xbmc
import xbmcaddon
from ant.core import driver
from ant.core import node

from vpower.PowerMeterTx import PowerMeterTx
from vpower.SpeedCadenceSensorRx import SpeedCadenceSensorRx
from vpower.BtAtsPowerCalculator import BtAtsPowerCalculator
from vpower.KurtKineticPowerCalculator import KurtKineticPowerCalculator
from vpower.TacxBlueMotionPowerCalculator import TacxBlueMotionPowerCalculator
from vpower import config
import sys

global antnode
global speed_sensor
global power_meter
antnode = None
speed_sensor = None
power_meter = None
monitor = xbmc.Monitor()
addon = xbmcaddon.Addon('service.vpower')


def start():
    global antnode
    global speed_sensor
    global power_meter
    from vpower.config import DEBUG, LOG, NETKEY, POWER_CALCULATOR, POWER_SENSOR_ID, SENSOR_TYPE, SPEED_SENSOR_ID
    xbmc.log("Using " + POWER_CALCULATOR.__class__.__name__, level=xbmc.LOGDEBUG)
    stick = driver.USB2Driver(None, log=LOG, debug=DEBUG)
    antnode = node.Node(stick)
    xbmc.log("Starting ANT node", level=xbmc.LOGDEBUG)
    antnode.start()
    key = node.NetworkKey('N:ANT+', NETKEY)
    antnode.setNetworkKey(0, key)

    xbmc.log("Starting speed sensor", level=xbmc.LOGDEBUG)

    # Create the speed sensor object and open it
    speed_sensor = SpeedCadenceSensorRx(
        antnode, SENSOR_TYPE, SPEED_SENSOR_ID)
    speed_sensor.open()
    # Notify the power calculator every time we get a speed event
    speed_sensor.notify_change(POWER_CALCULATOR)

    xbmc.log("Starting power meter with ANT+ ID " +
             repr(POWER_SENSOR_ID), level=xbmc.LOGDEBUG)

    # Create the power meter object and open it
    power_meter = PowerMeterTx(antnode, POWER_SENSOR_ID)
    power_meter.open()

    # Notify the power meter every time we get a calculated power value
    POWER_CALCULATOR.notify_change(power_meter)


def stop():
    global antnode
    global speed_sensor
    global power_meter
    if speed_sensor:
        xbmc.log("Closing speed sensor", level=xbmc.LOGDEBUG)
        speed_sensor.close()
        speed_sensor.unassign()
        speed_sensor = None
    if power_meter:
        xbmc.log("Closing power meter", level=xbmc.LOGDEBUG)
        power_meter.close()
        power_meter.unassign()
        power_meter = None
    if antnode:
        xbmc.log("Stopping ANT node", level=xbmc.LOGDEBUG)
        antnode.stop()
        antnode = None


def set_settings():
    # most of the config set here directly, vpower.cfg won't be loaded
    if addon.getSetting('speed_sensor_type') == '1':
        # speed only
        config.SENSOR_TYPE = 123
    else:
        # speed and cadence
        config.SENSOR_TYPE = 121
    config.VPOWER_DEBUG = False
    config.DEBUG = False
    try:
        config.SPEED_SENSOR_ID = int(addon.getSetting('speed_sensor_id'))
    except ValueError:
        config.SPEED_SENSOR_ID = None
    if addon.getSetting('trainer_type') == '1':
        config.POWER_CALCULATOR = globals()['BtAtsPowerCalculator']()
    elif addon.getSetting('trainer_type') == '2':
        config.POWER_CALCULATOR = globals()['TacxBlueMotionPowerCalculator']()
    else:
        config.POWER_CALCULATOR = globals()['KurtKineticPowerCalculator']()
    config.POWER_CALCULATOR.air_density = 1.191
    config.POWER_CALCULATOR.air_density_update_secs = 10
    config.POWER_CALCULATOR.wheel_circumference = int(
        addon.getSetting('wheel_circumference')
    ) / 1000.0
    config.POWER_CALCULATOR.set_correction_factor(1.0)
    config.POWER_CALCULATOR.set_debug(config.DEBUG or config.VPOWER_DEBUG)


if __name__ == '__main__':
    while not monitor.abortRequested():
        set_settings()
        if not config.SPEED_SENSOR_ID or not config.POWER_CALCULATOR.wheel_circumference:
            addon.openSettings()
        else:
            break
        if monitor.waitForAbort(10):
            break
    xbmc.log("Speed sensor %d - %d" % (config.SENSOR_TYPE,
                                       config.SPEED_SENSOR_ID), level=xbmc.LOGDEBUG)
    
    while not monitor.abortRequested():
        try:
            xbmc.log("Starting ANT...", level=xbmc.LOGDEBUG)
            start()
            xbmc.log("ANT started", level=xbmc.LOGDEBUG)
            break
        except:
            xbmc.log("Failed to start ANT. " +
                        traceback.format_exc(), level=xbmc.LOGERROR)
            if monitor.waitForAbort(10):
                break

    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            xbmc.log("Waiting to stop", level=xbmc.LOGDEBUG)
            break
    try:
        xbmc.log("Stopping ANT...", level=xbmc.LOGDEBUG)
        stop()
        xbmc.log("ANT stopped", level=xbmc.LOGDEBUG)
    except:
        xbmc.log("Failed to stop ANT. " +
                    traceback.format_exc(), level=xbmc.LOGERROR)
