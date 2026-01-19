# Project: Nugu Home (ng-home)
# Description: Network presence and security monitor for Discord
# Author: Simone Onorato (Nyokkimon)
# License: GPLv3
# Repository: https://github.com/nyokkimon/ng-home

import nmap
import socket
import updateConfig


def getLocalNetwork():
    """Detects the local IP and returns the /24 network range."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        localIp = s.getsockname()[0]
        s.close()

        dotSplit = localIp.split('.')
        networkRange = f"{dotSplit[0]}.{dotSplit[1]}.{dotSplit[2]}.0/24"
        return networkRange
    except Exception:
        return "192.168.1.0/24"


def executeScan():
    knownDevices = updateConfig.getDevices()
    networkRange = getLocalNetwork()

    nm = nmap.PortScanner()
    print(f"[LOG] ng-home: Auto-detected network: {networkRange}")

    # -sn: Ping scan, -PR: ARP discovery
    nm.scan(hosts=networkRange, arguments='-sn -PR')

    scanResults = []

    for host in nm.all_hosts():
        addressInfo = nm[host]['addresses']
        ipAddress = addressInfo.get('ipv4')
        macAddress = addressInfo.get('mac', 'UNKNOWN').upper()

        # --- FIX: Fallback Identifier ---
        # If MAC is UNKNOWN, we use the IP as the unique ID for registration
        deviceId = macAddress if macAddress != 'UNKNOWN' else ipAddress

        # Get Vendor
        vendor = nm[host].get('vendor', {}).get(macAddress, "Unknown Vendor")

        # Get Hostname
        hostnames = nm[host].hostnames()
        hostname = hostnames[0]['name'] if hostnames else "No Hostname"

        # Check if known using our Device ID (MAC or IP)
        isKnown = deviceId in knownDevices
        deviceName = knownDevices.get(deviceId, {}).get('userName', 'Nugu (Unknown)')

        scanResults.append({
            "ip": ipAddress,
            "mac": macAddress,
            "deviceId": deviceId, # Pass this to the alert formatter
            "vendor": vendor,
            "hostname": hostname,
            "name": deviceName,
            "isKnown": isKnown
        })

    return scanResults