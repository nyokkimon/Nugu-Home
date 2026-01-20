# Project: Nugu Home (Nugu-Home)
# Description: Network presence and security monitor for Discord
# Author: Simone Onorato (Nyokkimon)
# License: GPLv3
# Repository: https://github.com/nyokkimon/Nugu-Home

import json
import os

configPath = 'ngConfigs/configs.json'
devicesPath = 'ngConfigs/devices.json'


def getConfigs():
    with open(configPath, 'r') as f:
        return json.load(f)


def updateSetting(key, value):
    data = getConfigs()
    data[key] = value
    with open(configPath, 'w') as f:
        json.dump(data, f, indent=4)


def getDevices():
    if not os.path.exists(devicesPath):
        return {}
    with open(devicesPath, 'r') as f:
        return json.load(f)


def addDevice(identifier, nickname):
    devices = getDevices()
    # Normalize identifier to uppercase (standard for MACs/IPs)
    devices[identifier.upper()] = {"userName": nickname}
    with open(devicesPath, 'w') as f:
        json.dump(devices, f, indent=4)


def removeDevice(search_term):
    """
    Removes a device by searching for its MAC/IP ID OR its Nickname.
    """
    devices = getDevices()
    target_key = None

    # Normalize search term for comparison
    search_term_upper = search_term.upper()

    # 1. Check if the search term is a direct ID (MAC or IP)
    if search_term_upper in devices:
        target_key = search_term_upper

    # 2. If not found, search through the nicknames (userName)
    else:
        for device_id, info in devices.items():
            if info.get('userName', '').upper() == search_term_upper:
                target_key = device_id
                break

    # 3. If we found a match (either by ID or Nickname), delete it
    if target_key:
        del devices[target_key]
        with open(devicesPath, 'w') as f:
            json.dump(devices, f, indent=4)
        return True

    return False