# 🏠 Nugu Home (ㄴㄱ)
**The "Who's Home?" Network Monitor for Discord.**

**ng-home** is a network presence and security monitor for Discord. Named after the Korean word *Nugu* (누구 or ㄴㄱ- "Who?",), it tracks who is currently home and alerts you to unrecognized devices. It provides a rolling history of network activity while automatically keeping your Discord channel clean.

## 👤 Author & License
* **Creator:** Simone Onorato ([Nyokkimon](https://github.com/nyokkimon))
* **License:** [GPLv3](LICENSE) - Free to use and modify.


## ✨ Features
- **Presence Tracking:** Differentiates between known family devices (Green ✅) and unknown intruders (Orange ⚠️).
- **Vendor Detection:** Automatically identifies device manufacturers (Apple, Samsung, Sony, etc.).
- **Live Timestamps:** Every device card shows the exact "Scan Time."
- **Auto-Cleanup:** Automatically purges messages older than a set number of days to keep your channel clutter-free.
- **Smart Formatting:** Uses YAML-style blocks for easy reading on both mobile and desktop.

## 🛠️ Prerequisites

**Create the** `nugu` folder to store the bot and navigate to it.
1. **Clone the Repo:** `git clone https://github.com/nyokkimon/ng-home.git`
2. **Install Dependencies:** `pip install -r requirements.txt`

### Linux (Raspberry Pi / Ubuntu)
1. Install Nmap: `sudo apt install nmap`
2. Run with sudo: `sudo python3 bot.py` (Required for ARP/MAC scanning).

### Windows
1. Install Nmap from [nmap.org](https://nmap.org/download.html) (Ensure **Npcap** is checked during install).
2. Open Terminal or PowerShell as **Administrator**.
3. Run: `python bot.py`

## 🚀 Setup
1. **Install Requirements:**
   ```bash
   pip install discord.py python-nmap requests

2. **Discord Bot Configuration:**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Create a **New Application** and give it a name (e.g., `ng-home`).
   - Navigate to the **Bot** tab.
   - Enable **Message Content Intent** (This is required for the bot to read your `!add` and `!scan` commands).
   - Copy your **Token** and keep it safe.
   - Invite the bot to your server using the OAuth2 URL Generator with `Manage Messages` and `Send Messages` permissions.

3. **Local Configuration:**
   - On first run, the app will ask for the `token` and `channelId`. This will allow for automatic creation of config files.
   - *Note: Ensure the `channelId` is a number, not a string (no quotes).*

## 🔄 Updating
**Nugu Home** will automatically check for updates once every 24 hours. If a new version is detected, a notification will appear in your Discord channel.

To update without losing your registered devices or settings, follow these steps:

### Method 1: Manual Update (No Git)
1. **Download:** Go to the [Nugu Home GitHub](https://github.com/nyokkimon/ng-home) and download the latest repository as a ZIP.
2. **Extract:** Open the ZIP file.
3. **Overwrite:** Copy all the `.py` files and paste them into your existing project folder, choosing **"Replace/Overwrite"** when prompted.
4. **⚠️ Important:** **DO NOT** delete or overwrite your `ngConfigs/` folder. This folder contains your private tokens and device database.
5. **Restart:** Run `python bot.py`. The bot will automatically detect if any new settings need to be added to your configuration.

### Method 2: Git Update
If you cloned the repository using Git, simply navigate to the nugu folder and run:
`git pull`

*Note: Your ngConfigs/ folder is protected by the .gitignore file and will not be touched by Git.*

### 🛠️ Config Migration
Don't worry about new settings! Nugu Home features a built-in migration system. When you update to a version that requires new configuration keys, the bot will automatically "inject" them into your existing configs.json without erasing your Token or Channel ID.


## 🎮 Commands
| Command | Usage | Description                                                              |
| :--- | :--- |:-------------------------------------------------------------------------|
| `!nugu` | `!nugu` | Displays the help menu with all available options.                       |
| `!scan` | `!scan` | Triggers an immediate network scan and shows who is currently home.      |
| `!add` | `!add [MAC] [Name]` | Registers a device nickname (e.g., `!add 00:AA:BB... Dad's Phone`).      |
| `!remove` | `!remove [MAC]` | Removes a registered device from the "Known" database.                   |
| `!frequency`| `!frequency [Min]` | Changes how often the bot scans automatically (e.g., `!frequency 120`). Use 0 for Manual Mode. |
| `!history` | `!history [Days]` | Sets the data retention limit (e.g., `!history 1` for a clean channel).  |

## 📝 How it Works
1. **Network Discovery:** The bot utilizes `python-nmap` to perform an ARP scan of your local subnet.
2. **Database Comparison:** It checks every discovered MAC address against your `devices.json` file.
3. **Presence Reporting:**
    * **Known Devices:** Posted with a **Green Status** and the nickname you assigned.
    * **Unknown Devices:** Posted with a **Warning Status** and a prompt to register them.
4. **Automated Maintenance:** Before every scheduled scan, the bot calculates the "Cutoff Date" based on your `historyDays` setting and purges all expired messages to prevent channel clutter.

### Manual vs Automated
-   If `scanFrequency = 0`, all background tasks stop and the bot waits
    for `!scan`.
-   If greater than `0`, scans run automatically on a timed loop.

------------------------------------------------------------------------

## 🤝 Contributors

Huge thanks to everyone who helped shape **Nugu Home**:

-   **[Simone Onorato (Nyokkimon)](https://www.youtube.com/@Nyokkimon)** --- Project Lead & Creator

------------------------------------------------------------------------

## ⚖️ License

This project is licensed under the **GPLv3 License**.\
See the `LICENSE` file for details.
