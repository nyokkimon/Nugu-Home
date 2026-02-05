# 🏠 Nugu Home (ㄴㄱ)
**The "Who's Home?" Network Monitor for Discord.**

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/nyokkimon)

**Nugu-Home** is a network presence and security monitor for Discord. Named after the Korean word *Nugu* (누구 or ㄴㄱ- "Who?",), it tracks who is currently home and alerts you to unrecognized devices. It provides a rolling history of network activity while automatically keeping your Discord channel clean.

## Video Tutorial
📺 Watch here: https://www.youtube.com/watch?v=Jfk1FQ2KWM0

## Logo
🖼️ Download and use the project logo here:  
https://github.com/nyokkimon/Nugu-Home/blob/main/assets/logo/Nugu-logo_highRes.png


## 👤 Author & License
* **Creator:** Simone Onorato ([Nyokkimon](https://github.com/nyokkimon))
* **License:** [GPLv3](LICENSE) - Free to use and modify.


## ✨ Features
- **Presence Tracking:** Differentiates between known family devices (Green ✅) and unknown intruders (Orange ⚠️).
- **Vendor Detection:** Automatically identifies device manufacturers (Apple, Samsung, Sony, etc.).
- **Live Timestamps:** Every device card shows the exact "Scan Time."
- **Auto-Cleanup:** Automatically purges messages older than a set number of days to keep your channel clutter-free.
- **Smart Formatting:** Uses YAML-style blocks for easy reading on both mobile and desktop.

---

## 🚀 Installation & Setup

### 1. Discord Bot Configuration
Before running the code, you must prepare the Discord environment:

### A. Server & Private Channel Setup
1. **Enable Developer Mode:** In your Discord App, go to **User Settings** > **Advanced** > Toggle **Developer Mode** to **ON**.
2. **Create a Server:** Click the plus (+) icon on the left sidebar, select Create My Own, then For me and my friends and name it `Nugu-Home`.
3. **Create a Private Channel:** In your server, click the **+** next to Text Channels. Toggle **Private Channel** to **ON** and name it `nugu-home`.
4. **Get Channel ID:** Right-click the `#nugu-home` channel name and select **Copy Channel ID**. Save this for the setup wizard.

### B. Create the Application
1. Go to the <a href="https://discord.com/developers/applications" target="_blank">Discord Developer Portal</a>.
2. Click **New Application** and name it `Nugu-Home`.
3. **The Bot Token:** Navigate to the **Bot** tab. Click **Reset Token** to generate your unique key. **Copy and save this**—it is the only time you will see it.
4. **Intents (Crucial):** Scroll down to **Privileged Gateway Intents** and toggle **Message Content Intent** to **ON**. Click **Save Changes**.

### C. Generate the Invite Link
1. Navigate to **OAuth2** -> **URL Generator**.
2. **Scopes:** Select `bot`.
3. **Bot Permissions:** A list will appear. Under "Text Permissions," select **Send Messages** and **Manage Messages**.
4. Copy the URL generated at the bottom. Paste it into your browser, select your server, and click **Authorize**.

### D. Invite the Bot to the Channel
1. Go to your private channel, click on the gear whell **Edit Channel** > **Permissions** > **Add Members** 
2. Select **Nugu-Home** APP. (The bot cannot post in private channels unless manually added).
---

[PRE] Start by getting sudo admin privileges
* **Linux (Raspberry Pi / Ubuntu):**
    ```bash
    sudo su
    ```

### 2. Install Network Dependencies (Nmap)
The bot requires Nmap to perform network discovery.
* **Linux (Raspberry Pi / Ubuntu):**
    ```bash
    apt update && sudo apt install nmap -y
    ```

### 3. Local Project Setup

1.  **Clone the Repo:**
    ```bash
    git clone https://github.com/nyokkimon/Nugu-Home.git
    cd Nugu-Home
    ```

2.  **Create Virtual Environment**
* **Linux (Raspberry Pi / Ubuntu):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python Libraries:**
    ```bash
    pip install -r requirements.txt
    ```

### 4. Running the Bot
The bot **requires administrative/root privileges** to perform ARP/MAC address scanning.
Ensure that the **virtual environment is active before** running the bot.

* **Linux:**
    ```bash
    python3 bot.py
    ```

### 5. First-Run Wizard
On the first launch, the bot will start a Setup Wizard in your terminal:
1.  **Token:** Paste your Discord Bot Token.
2.  **Channel ID:** Paste the ID of your private Discord channel.
    * *Note: Ensure the `channelId` is a raw number (e.g., `123456789012345678`), do not use quotes.*

---


## 🤖 Simplified Auto-Start Setup
Follow these steps to ensure your bot starts automatically when your computer or Raspberry Pi reboots.


### 🐧 Linux: Using Supervisor
Supervisor is the easiest way to keep your bot running in the background. It will automatically restart the bot if it crashes.

1. **Install Supervisor:**
   ```bash
   sudo apt update && sudo apt install supervisor -y
   ```
2. **Create the Configuration File:**
    ```bash
    sudo nano /etc/supervisor/conf.d/nugu.conf
    ```
3. **Paste the following (Update YOUR_USER to your actual username):**
    ```Ini, TOML
    [program:nugu]
    command=/home/YOUR_USER/Nugu-Home/venv/bin/python3 bot.py
    directory=/home/YOUR_USER/Nugu-Home
    autostart=true
    autorestart=true
    user=root
    stderr_logfile=/var/log/nugu.err.log
    stdout_logfile=/var/log/nugu.out.log
    ```
4. **Apply the changes:**
    ```bash
    sudo supervisorctl reread
    sudo supervisorctl update
    ```
---


## 🔄 Updating
**Nugu Home** will automatically check for updates once every 24 hours. If a new version is detected, a notification will appear in your Discord channel.

To update without losing your registered devices or settings, follow these steps:

### Method 1: Manual Update (No Git)
1. **Download:** Go to the [Nugu Home GitHub](https://github.com/nyokkimon/Nugu-Home) and download the latest repository as a ZIP.
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
