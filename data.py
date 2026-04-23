#imports
from colorama import Fore, Style
import colorama
import os
import subprocess
import requests
colorama.init(autoreset=True)
#vars
mc_process = None
intro = f"""{Fore.CYAN}{Style.BRIGHT}
███████╗███████╗██╗  ██╗███████╗██╗  ██╗ ██████╗ ███████╗████████╗
╚══███╔╝██╔════╝██║ ██╔╝██╔════╝██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
  ███╔╝ █████╗  █████╔╝ █████╗  ███████║██║   ██║███████╗   ██║
 ███╔╝  ██╔══╝  ██╔═██╗ ██╔══╝  ██╔══██║██║   ██║╚════██║   ██║
███████╗███████╗██║  ██╗███████╗██║  ██║╚██████╔╝███████║   ██║
╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝

{Fore.MAGENTA}        One Click Minecraft Server Launcher
{Fore.YELLOW}              Python Powered • Local Host
{Fore.GREEN}                 No Pain • Just Launch

{Fore.RED}                    [1] Start Server
{Fore.RED}                    [2] Exit
{Fore.RED}                    [3] Creators YT
"""
inputfile = f"""{Fore.CYAN}{Style.BRIGHT}
              Choose a Option
"""
BASE_DIR = "minecraft_files"
SERVER_JAR = os.path.join(BASE_DIR, "server.jar")

#def
def clearscreen():
    os.system("cls" if os.name == "nt" else "clear")
def startsplashscreen():
    clearscreen()
    print(intro)
def openyt():
    yt = f"""
    {Fore.RED}       https://youtube.com/@zekelabsyt     
    """
    print(yt)
def download_latest_paper():
    print("Fetching latest Paper version...")

    project_url = "https://api.papermc.io/v2/projects/paper"
    project_data = requests.get(project_url).json()

    if not project_data.get("versions"):
        print("No versions found ❌")
        return

    latest_version = project_data["versions"][-1]
    print(f"Latest version: {latest_version}")

    version_url = f"https://api.papermc.io/v2/projects/paper/versions/{latest_version}"
    version_data = requests.get(version_url).json()

    if not version_data.get("builds"):
        print("No builds found ❌")
        return

    latest_build = version_data["builds"][-1]
    print(f"Latest build: {latest_build}")

    jar_name = f"paper-{latest_version}-{latest_build}.jar"

    download_url = (
        f"https://api.papermc.io/v2/projects/paper/"
        f"versions/{latest_version}/builds/{latest_build}/downloads/{jar_name}"
    )

    print("Downloading server.jar...")
    print(download_url)

    os.makedirs(BASE_DIR, exist_ok=True)

    response = requests.get(download_url)

    with open(SERVER_JAR, "wb") as f:
        f.write(response.content)

    print("Done 😎")

def ispaperinstalled():
    server_path = "minecraft_files/server.jar"

    if os.path.exists(server_path):
        return True
    else:
        return False
def startserver():
    ispaper = ispaperinstalled()
    if ispaper == True:
        mc()
    else:
        download_latest_paper()
        startserver()
def accepteula():
    eula_path = os.path.join("minecraft_files", "eula.txt")

    with open(eula_path, "w") as f:
        f.write("eula=true")

    print("EULA accepted ✅")
import threading
import subprocess
import os
from colorama import Fore

mc_process = None


def accepteula():
    eula_path = os.path.join("minecraft_files", "eula.txt")

    with open(eula_path, "w") as f:
        f.write("eula=true")

    print(f"{Fore.GREEN}EULA accepted ✅")


def readlogs():
    global mc_process

    try:
        for line in mc_process.stdout:
            print(line.strip())
    except Exception as e:
        print(f"{Fore.RED}Log reader failed: {e}")


def mc():
    global mc_process

    accepteula()

    server_path = os.path.join("minecraft_files", "server.jar")

    if not os.path.exists(server_path):
        print(f"{Fore.RED}server.jar not found ❌")
        return

    print(f"{Fore.GREEN}Starting Minecraft Server... 😎")
    print(f"{Fore.CYAN}Local Server IP: localhost:25565")
    print(f"{Fore.CYAN}LAN IP: use your PC local IP + :25565")

    try:
        mc_process = subprocess.Popen(
            [
                "java",
                "-Xmx4G",
                "-Xms2G",
                "-jar",
                "server.jar",
                "nogui"
            ],
            cwd="minecraft_files",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        print(f"{Fore.GREEN}Server started ✅")
        print(f"{Fore.YELLOW}Type commands directly below ↓")

                # logs run in background
        log_thread = threading.Thread(target=readlogs, daemon=True)
        log_thread.start()

        # keep program alive while server runs
        while True:
            if mc_process.poll() is not None:
                print(f"{Fore.RED}Server stopped ❌")
                break

    except Exception as e:
        print(f"{Fore.RED}Error starting server: {e}")
