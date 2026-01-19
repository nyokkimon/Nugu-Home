# Project: Nugu Home (ng-home)
# Description: Network presence and security monitor for Discord
# Author: Simone Onorato (Nyokkimon)
# License: GPLv3
# Repository: https://github.com/nyokkimon/ng-home

import discord
from discord.ext import commands, tasks
import ngScanner
import updateConfig
import discordAlerts
import asyncio
import os
import sys
import json
import requests
from datetime import datetime, timedelta, timezone

# --- CONSTANTS ---
VERSION = "1.0"
REPO_URL = "https://github.com/nyokkimon/ng-home"
RAW_VERSION_URL = "https://raw.githubusercontent.com/nyokkimon/ng-home/main/version.txt"


# --- CONFIGURATION BOOTSTRAPPER ---
def ensure_config_persistence():
    config_dir = 'ngConfigs'
    config_path = os.path.join(config_dir, 'configs.json')
    blueprint = {"botToken": "", "channelId": 0, "scanFrequency": 60, "historyDays": 7}

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    if not os.path.exists(config_path):
        print("🏠 --- Nugu Home (ㄴㄱ) Setup Wizard ---")
        token = input("🔑 Enter your Discord Bot Token: ").strip()
        channel = input("📺 Enter the Discord Channel ID: ").strip()
        blueprint["botToken"] = token
        blueprint["channelId"] = int(channel) if channel.isdigit() else 0
        with open(config_path, 'w') as f:
            json.dump(blueprint, f, indent=4)
    else:
        with open(config_path, 'r') as f:
            try:
                user_config = json.load(f)
            except json.JSONDecodeError:
                user_config = {}
        updated = False
        for key, value in blueprint.items():
            if key not in user_config:
                user_config[key] = value
                updated = True
        if updated:
            with open(config_path, 'w') as f:
                json.dump(user_config, f, indent=4)


ensure_config_persistence()

# --- LOAD CONFIGS ---
appConfigs = updateConfig.getConfigs()
botToken = appConfigs.get('botToken')
channelId = appConfigs.get('channelId')

if not botToken:
    print("[CRITICAL] No botToken found. Please edit ngConfigs/configs.json and restart.")
    sys.exit()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# --- UPDATE LOGIC ---
async def check_for_updates(notify_dest=None):
    """Checks GitHub for a newer version. If notify_dest is None, it only logs to console."""
    try:
        response = requests.get(RAW_VERSION_URL, timeout=10)
        latest_version = response.text.strip()

        if latest_version > VERSION:
            print(f"\n[UPDATE] A new version ({latest_version}) is available!")
            if notify_dest:
                msg = (
                    f"🚀 **Update Available: v{latest_version}**\n"
                    f"To update safely, type `!update` for instructions.\n"
                )
                await notify_dest.send(msg)
                return True
    except Exception as e:
        print(f"[SYSTEM] Update check: {e}")
    return False


# --- TASKS ---
@tasks.loop(hours=24)
async def versionCheckTask():
    """Background task to check for updates silently once a day."""
    # We don't pass a destination here so it only logs to the terminal/console
    await check_for_updates()


@tasks.loop(minutes=60)
async def autoScanner():
    channel = bot.get_channel(channelId)
    if channel:
        await run_full_report(channel)


# --- HELPER FUNCTIONS ---
async def cleanup_channel(channel):
    days = updateConfig.getConfigs().get('historyDays', 7)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        await channel.purge(limit=1000, check=lambda m: m.created_at < cutoff)
    except Exception:
        pass


async def run_full_report(dest):
    """Universal function to scan and report with the desired visual order."""

    # 1. WELCOME MESSAGE
    await dest.send("👋 **Welcome to Nugu (ㄴㄱ), who is home?**\nTo list all commands type `!nugu`")

    # 2. SEPARATOR
    await dest.send("──────────────────────────────")
    await asyncio.sleep(0.5)

    # 3. UPDATE CHECK ( अनाउंसमेंट here)
    # We call it here so it appears exactly once between welcome and scan
    await check_for_updates(dest)
    await asyncio.sleep(0.5)

    current_configs = updateConfig.getConfigs()
    freq = current_configs.get('scanFrequency', 60)
    hist = current_configs.get('historyDays', 7)
    registered_count = len(updateConfig.getDevices())

    if isinstance(dest, discord.TextChannel):
        await cleanup_channel(dest)

    results = ngScanner.executeScan()
    active_count = len(results)

    # 4. SCAN HEADER
    header = discordAlerts.formatScanHeader(active_count, registered_count, freq, hist)
    await dest.send(header)
    await asyncio.sleep(1)

    if results:
        for device in results:
            msg = discordAlerts.formatKnownDevice(device) if device['isKnown'] else discordAlerts.formatNuguAlert(
                device)
            await dest.send(msg)
            await asyncio.sleep(0.7)
        await dest.send(f"\n📊 **Summary:** Presence check finished. {active_count} devices detected.")
    else:
        await dest.send("\n❌ **Scan Failed:** No devices detected.")


# --- EVENTS ---
@bot.event
async def on_ready():
    print(f'ng-home v{VERSION} is online as {bot.user.name}')
    if not versionCheckTask.is_running():
        versionCheckTask.start()

    current_freq = updateConfig.getConfigs().get('scanFrequency', 60)
    if current_freq > 0:
        autoScanner.change_interval(minutes=current_freq)
        if not autoScanner.is_running():
            autoScanner.start()
    else:
        print("[SYSTEM] Manual Mode enabled.")


# --- COMMANDS ---
@bot.command()
async def scan(ctx):
    await run_full_report(ctx.channel)


@bot.command()
async def update(ctx):
    embed = discord.Embed(title="🔄 How to Update", color=discord.Color.blue())
    embed.add_field(name="Method A: Git", value="Run `git pull` & restart.", inline=False)
    embed.add_field(name="Method B: Manual", value=f"[Download ZIP]({REPO_URL}), overwrite `.py` files.", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def history(ctx, days: int):
    updateConfig.updateSetting('historyDays', max(0, days))
    await ctx.send(f"🗑️ **History updated:** {days} days.")


@bot.command()
async def add(ctx, mac: str, *, name: str):
    updateConfig.addDevice(mac, name)
    await ctx.send(f"📝 **Registered:** `{name}`")


@bot.command()
async def remove(ctx, *, name_or_id: str):
    if updateConfig.removeDevice(name_or_id):
        await ctx.send(f"🗑️ **Removed:** `{name_or_id}`")
    else:
        await ctx.send(f"❌ **Error:** Not found.")


@bot.command()
async def frequency(ctx, minutes: float):
    mins = int(round(minutes))
    updateConfig.updateSetting('scanFrequency', mins)
    if mins == 0:
        if autoScanner.is_running(): autoScanner.stop()
        await ctx.send("🛑 **Manual Mode enabled.**")
    else:
        autoScanner.change_interval(minutes=mins)
        if not autoScanner.is_running(): autoScanner.start()
        await ctx.send(f"⏱ **Frequency:** {mins}m.")


@bot.command()
async def nugu(ctx):
    await ctx.send(embed=discordAlerts.getHelpEmbed())


try:
    bot.run(botToken)
except Exception as e:
    print(f"Bot failed: {e}")