# ZekeHost

One Click Minecraft Server Launcher

ZekeHost is a lightweight Python-powered Minecraft server launcher built for fast local hosting with less pain and more speed.

No Docker.
No complicated setup.
No suffering.
Just launch.

---

## Features

* Automatic latest PaperMC server download
* Automatic `eula.txt` acceptance
* Live Minecraft server console logs
* Direct command input from terminal
* Localhost + LAN hosting support
* Java version support for modern Minecraft
* Simple terminal UI with colored interface
* Creator shortcut to YouTube channel

---

## Requirements

* Python 3.10+
* Java 17+ (recommended Java 21)
* Internet connection (for first PaperMC download)

Recommended Java:

Eclipse Adoptium Temurin JDK

---

## Project Structure

```text
ZekeHost/
│
├── main.py
├── data.py
├── .gitignore
├── README.md
│
└── minecraft_files/
    ├── server.jar
    ├── eula.txt
    └── world/
```

---

## Installation

Clone the repo:

```bash
git clone https://github.com/zeke-youtube/ZekeHost.git
cd ZekeHost
```

Install dependencies:

```bash
pip install colorama requests
```

Make sure Java is installed:

```bash
java -version
```

Expected:

```text
Java 17+
```

---

## Usage

Run:

```bash
python main.py
```

You will see:

```text
[1] Start Server
[2] Exit
[3] Creators YT
```

Choose:

```text
1
```

and ZekeHost will:

* check for `server.jar`
* auto-download latest PaperMC if missing
* auto-accept EULA
* start the Minecraft server
* show live logs
* allow direct Minecraft commands

Example commands:

```text
op YourName
say Hello world
time set day
gamemode creative YourName
stop
```

---

## Notes

Default local server:

```text
localhost:25565
```

LAN players can join using:

```text
Your-PC-IP:25565
```

Example:

```text
192.168.1.100:25565
```

---

## Troubleshooting

### Minecraft requires Java 17+

Check Java path:

```bash
where java
```

Sometimes old Java 8 causes pain.

Use newer Java manually inside Python if needed.

---

### Boat Apocalypse

If your logs look like:

```text
[Acacia Boat: Summoned new Acacia Boat]
```

repeated 9000 times…

you probably created:

```text
Boat Apocalypse™
```

Fix with:

```text
kill @e[type=minecraft:acacia_boat]
gamerule commandBlockOutput false
```

---

## Future Ideas

* Flask web admin panel
* Remote dashboard
* Backup system
* Plugin manager
* World selector
* Auto restart
* Performance monitor
* Public hosting tools

---

## Philosophy

```text
Devs:
did I break something? yes
can I ship it? yes
```

---

## Built With

* Python
* PaperMC
* Java
* Terminal suffering
* questionable life decisions

---

## Creator

Built by Zeke

YouTube:
https://youtube.com/@zekelabsyt

GitHub:
https://github.com/zeke-youtube

---

## License

MIT

Probably.

Maybe.

We’ll see.
