
import sys

import requests
import time
from rcon.source import Client
import json
from pathlib import Path
serverip = None
serverrconport = None
serverport =None
serverpassword = None
discord_webhook_url = None
discordresponse= None
previous_status = None
previous_response = None

app_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
file_path = app_dir / "savefile.json"


if file_path.exists():
    print("File exists! Proceeding to load...")
    
  
    if file_path.stat().st_size == 0:
        print("File is empty, creating new data...")
        loaded_data = {
            "server_ip": None,
            "server_rconport": None,
            "server_password": None,
            "discord_webhook_url": None,
            "messageid": None,
            "serverport": None
        }
        
        with open("savefile.json", "w") as file:
                json.dump(loaded_data, file, indent=4)
                exit(1)
    else:
        with open("savefile.json", "r") as file:
            loaded_data = json.load(file)
        
else:
    data_to_save = {
    "server_ip": None,
    "server_rconport": None,
    "server_password": None,
    "discord_webhook_url": None,
    "messageid": None,
    "serverport": None
    }
    with open("savefile.json", "w") as file:
        json.dump(data_to_save, file, indent=4)
        print("File not found! Creating a new one...")
    exit(1)
print(loaded_data)



if loaded_data.get("messageid") is None:
    discordresponse = requests.post(discord_webhook_url+"?wait=true", json={"content": "Server status monitoring started!"})
    print(discordresponse.json)
    if discordresponse.status_code == 200:
        print("Initial message sent to Discord.")
        loaded_data["messageid"] = discordresponse.json().get("id")
        with open("savefile.json", "w") as file:
            json.dump(loaded_data, file, indent=4)





while True:
    status = "offline"
    response = "N/A"
    try:
        with Client(serverip, serverrconport, passwd=serverpassword, timeout=5.0) as client:
            response = client.run('players')
            print(response)
            status = "online"
    except Exception as e:
        status = "offline"
        print(f"Connection failed: {e}")
    

    if status != previous_status or response != previous_response:
        print(f"Status changed: {previous_status} -> {status}")

        
        webhook_data = {
                "embeds": [{
            "color": 65280 if status == "online" else 16711680,
                "timestamp": "2026-08-21T11:18:13.149Z",
                "url": "https://discord.com",
                "author": {
                    "name": "Zomboid Server Status",
                    "url": "https://discord.com",
                    "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png"
                },
                "thumbnail": {
                    "url": "https://cdn.discordapp.com/embed/avatars/0.png"
                },
                "footer": {
                    
                    "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png"
                },
                "fields": [
                    {
                        "name": "IP",
                        "value": "mauritania-gis.tun.ply.gg",
                        "inline": True
                    },
                    {
                        "name": "Port",
                        "value": loaded_data.get("serverport"),
                        "inline": True
                    },
                    {
                        "name": "Players",
                        "value": response,
                        "inline": False
                    }
                ]
            }
        ]
        }
        
        try:
            requests.patch(f"{discord_webhook_url}/messages/{loaded_data['messageid']}", json=webhook_data)
            print("Status posted to Discord")
        except Exception as e:
            print(f"Failed to post to Discord: {e}")
        
        previous_status = status
        previous_response = response


    time.sleep(10)

