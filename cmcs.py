import requests
import os

manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

def download_version(version_id):
    manifest = requests.get(manifest_url).json()
    version_url = next(v for v in manifest["versions"] if v["id"] == version_id)["url"]
    jar_url = requests.get(version_url).json()["downloads"]["server"]["url"]
    
    with open(f"server.jar", "wb") as f:
        f.write(requests.get(jar_url).content)

def create_start_server(max_ram, min_ram):
    with open("start.bat", 'a', encoding="utf-8") as f:
        f.write(f"java -Xmx{max_ram}M -Xms{min_ram}M -jar server.jar nogui")

def agree_eula():
    with open ('eula.txt', 'r') as f:
        old_data = f.read()
    new_data = old_data.replace('eula=false', 'eula=true')
    with open ('eula.txt', 'w') as f:
        f.write(new_data)

print(
"   _____ __  __  _____  _____ \n"
"  / ____|  \/  |/ ____|/ ____|\n"
" | |    | \  / | |    | (___  \n"
" | |    | |\/| | |     \___ \ \n"
" | |____| |  | | |____ ____) |\n"
"  \_____|_|  |_|\_____|_____/ \n"
"   Create MineCraft Server\n"
"--------------------------------")

download_version(str(input("Minecraft server version: ")))
print("Create start.bat")
create_start_server(input("Maximize RAM usage in MB: "), input("Minimal RAM usage in MB: "))
print("Launch start.bat")
os.system("start.bat")

if input("Do you agree with the eula: \"https://aka.ms/MinecraftEULA\"? (Answer \"yes\" or \"no\"): ").lower() == "yes":
    agree_eula()
else:
    exit(0)

print("Minecraft server is ready. Launch it via start.bat")