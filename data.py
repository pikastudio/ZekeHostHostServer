# imports
from colorama import Fore, Style
import colorama
import os
import subprocess
import requests
import threading
import time

colorama.init(autoreset=True)

# vars
BASE_DIR = "minecraft_files"
SERVER_JAR = os.path.join(BASE_DIR, "server.jar")
CLOUDFLARED_PATH = "cf/cloudflared.exe"

mc_process = None
tunnel_process = None

# -------------------------
# UI
# -------------------------
def clearscreen():
    os.system("cls" if os.name == "nt" else "clear")

def splash():
    clearscreen()
    print(f"""{Fore.CYAN}{Style.BRIGHT}
Zeke MC Launcher 😎
""")

# -------------------------
# Paper download
# -------------------------
def download_latest_paper():
    print("Fetching latest Paper version...")

    project_data = requests.get("https://api.papermc.io/v2/projects/paper").json()
    latest_version = project_data["versions"][-1]

    version_data = requests.get(
        f"https://api.papermc.io/v2/projects/paper/versions/{latest_version}"
    ).json()

    latest_build = version_data["builds"][-1]
    jar_name = f"paper-{latest_version}-{latest_build}.jar"

    download_url = f"https://api.papermc.io/v2/projects/paper/versions/{latest_version}/builds/{latest_build}/downloads/{jar_name}"

    print(f"Downloading {jar_name}...")

    os.makedirs(BASE_DIR, exist_ok=True)

    r = requests.get(download_url)
    with open(SERVER_JAR, "wb") as f:
        f.write(r.content)

    print("Done 😎")

# -------------------------
# EULA
# -------------------------
def accepteula():
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(os.path.join(BASE_DIR, "eula.txt"), "w") as f:
        f.write("eula=true")
    print(f"{Fore.GREEN}EULA accepted ✅")

# -------------------------
# Cloudflare Tunnel
# -------------------------
def start_tunnel():
    global tunnel_process

    if not os.path.exists(CLOUDFLARED_PATH):
        print(f"{Fore.RED}cloudflared.exe not found ❌")
        return

    print(f"{Fore.YELLOW}Starting Cloudflare tunnel...")

    tunnel_process = subprocess.Popen(
        [CLOUDFLARED_PATH, "tunnel", "--url", "tcp://localhost:25565"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in tunnel_process.stdout:
        print(line.strip())

        if "trycloudflare.com" in line:
            print(f"\n{Fore.GREEN}🌍 PUBLIC IP ABOVE ↑\n")
            break

# -------------------------
# Logs
# -------------------------
def readlogs():
    global mc_process
    try:
        for line in mc_process.stdout:
            print(line.strip())
    except Exception as e:
        print(f"{Fore.RED}Log reader failed: {e}")

# -------------------------
# Start Server
# -------------------------
def mc():
    global mc_process

    if not os.path.exists(SERVER_JAR):
        download_latest_paper()

    accepteula()

    print(f"{Fore.GREEN}Starting Minecraft Server... 😎")
    print(f"{Fore.CYAN}Local: localhost:25565")

    try:
        mc_process = subprocess.Popen(
            [
                "java",
                "-Xmx2G",
                "-Xms1G",
                "-jar",
                "server.jar",
                "nogui"
            ],
            cwd=BASE_DIR,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        print(f"{Fore.GREEN}Server started ✅")

        # logs
        threading.Thread(target=readlogs, daemon=True).start()

        # wait before tunnel
        time.sleep(5)
        start_tunnel()

        # keep alive
        while True:
            if mc_process.poll() is not None:
                print(f"{Fore.RED}Server stopped ❌")
                break
            time.sleep(1)

    except Exception as e:
        print(f"{Fore.RED}Error starting server: {e}")

    if tunnel_process:
        tunnel_process.terminate()

# -------------------------
# Public entry
# -------------------------
def startserver():
    splash()
    mc()
