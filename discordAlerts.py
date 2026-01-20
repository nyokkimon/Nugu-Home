# Project: Nugu Home (Nugu-Home)
# Description: Network presence and security monitor for Discord
# Author: Simone Onorato (Nyokkimon)
# License: GPLv3
# Repository: https://github.com/nyokkimon/Nugu-Home

import discord
from datetime import datetime


def getHelpEmbed():
    """Returns the pretty help menu card including all user commands."""
    embed = discord.Embed(
        title="🏠 Nugu-Home (Nugu Home) Guide",
        description="Monitor your home network from anywhere.",
        color=discord.Color.blue()
    )
    embed.add_field(name="🚀 `!scan`", value="Trigger a manual network scan.", inline=False)
    embed.add_field(name="📝 `!add [ID] [Name]`", value="Register a new device using its MAC or IP ID.", inline=False)
    embed.add_field(name="🗑️ `!remove [Nickname/ID]`", value="Remove a device by its Name or ID.", inline=False)
    embed.add_field(name="⏱ `!frequency [Min]`", value="Change the scan interval.", inline=False)
    embed.add_field(name="📜 `!history [Days]`", value="Set how many days of logs to keep.", inline=False)
    embed.add_field(name="🔄 `!update`", value="Show update instructions.", inline=False)

    embed.set_footer(text="Nugu-Home: Who is on my network?")
    return embed


def formatScanHeader(total_active, total_registered, frequency, history):
    """Creates a clean status header with no leading padding."""
    return (
        f"📡 **Nugu-Home: Presence Check Initiated**\n"
        f"```status\n"
        f"Active: {total_active} | Registered: {total_registered}\n"
        f"Interval: {frequency} | History: {history} days\n"
        f"```"
    )


def formatNuguAlert(device):
    """Formats the alert message for an UNKNOWN device."""
    now = datetime.now().strftime("%H:%M:%S")
    return (
        f"⚠️ **Nugu-Home: NEW DEVICE DETECTED!**\n"
        f"```yaml\n"
        f"IP:       {device['ip']}\n"
        f"MAC:      {device['mac']}\n"
        f"Vendor:   {device['vendor']}\n"
        f"Hostname: {device['hostname']}\n"
        f"```\n"
        f"**To register this device, use:**\n"
        f"`!add {device['deviceId']} Nickname`\n"
        f"*Scan time: {now}*\n"
        f"──────────────────────────────"
    )


def formatKnownDevice(device):
    """Formats the status message for a REGISTERED device."""
    now = datetime.now().strftime("%H:%M:%S")
    return (
        f"✅ **Nugu-Home: {device['name']} is online**\n"
        f"```yaml\n"
        f"Status:   Recognized\n"
        f"IP:       {device['ip']}\n"
        f"MAC:      {device['mac']}\n"
        f"Vendor:   {device['vendor']}\n"
        f"Hostname: {device['hostname']}\n"
        f"```\n"
        f"*Scan time: {now}*\n"
        f"──────────────────────────────"
    )