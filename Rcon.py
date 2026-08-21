
import sys
import threading
import requests
from rcon.source import Client
import json
from pathlib import Path


discordresponse= None
previous_status = None
previous_response = None
exitapp = False
pollrateinseconds = 10
stop_event = threading.Event()

app_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
file_path = app_dir / "savefile.json"
#Running command and printing its return

def exitevent(state):
    global exitapp
    exitapp = state
    if state:
        stop_event.set()
        print("Exiting application...")
        sys.exit(0)

def runcommand(command):
    try:
        with Client(loaded_data.get("server_ip"), loaded_data.get("server_rconport"), passwd=loaded_data.get("server_password"), timeout=5.0) as client:
            commandresponse = client.run(command)
            print(commandresponse)
    except Exception as e:
        print(f"Failed to execute command '{command}': {e}")

#keep running in background to check if command is entered and run it in a new thread

def commandenter():
    while True:
        command = input("")
        if command.lower() == 'exit':
            print("Quitting application...")
            stop_event.set()
        else:
            threading.Thread(target=runcommand, args=(command,)).start()


threading.Thread(target=commandenter, daemon=True).start()

if file_path.exists():
    print("File exists! Proceeding to load...")
    
  
    if file_path.stat().st_size == 0:
        print("File is empty, creating new data...")
        loaded_data = {
            "server_ip": None,
            "altenative_server_ip": None,
            "server_rconport": None,
            "server_password": None,
            "discord_webhook_url": None,
            "messageid": None,
            "serverport": None
        }
        
        with open(file_path, "w") as file:
                json.dump(loaded_data, file, indent=4)
                stop_event.set()
    else:
        with open(file_path, "r") as file:
            loaded_data = json.load(file)
        
else:
    data_to_save = {
    "server_ip": None,
    "altenative_server_ip": None,
    "server_rconport": None,
    "server_password": None,
    "discord_webhook_url": None,
    "messageid": None,
    "serverport": None
    }
    with open(file_path, "w") as file:
        json.dump(data_to_save, file, indent=4)
        print("File not found! Creating a new one...")
    stop_event.set()


if loaded_data.get("messageid") is None:
    discordresponse = requests.post(loaded_data.get("discord_webhook_url")+"?wait=true", json={"content": "Server status monitoring started!"})
    print(discordresponse.json)
    if discordresponse.status_code == 200:
        print("Initial message sent to Discord.")
        loaded_data["messageid"] = discordresponse.json().get("id")
        with open(file_path, "w") as file:
            json.dump(loaded_data, file, indent=4)

if loaded_data.get("alternate_server_ip") is None:
    print("Alternate server IP not set, using primary server IP as fallback.")
    print(f"Primary server IP: {loaded_data.get('server_ip')}")
    loaded_data["alternate_server_ip"] = loaded_data.get("server_ip")
    print(f"Alternate server IP set to: {loaded_data.get('alternate_server_ip')}")




while stop_event.is_set() == False:
    status = "offline"
    response = "N/A"
    try:
        with Client(loaded_data.get("server_ip"), loaded_data.get("server_rconport"), passwd=loaded_data.get("server_password"), timeout=5.0) as client:
            response = client.run('players')
            
            if response != previous_response:
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
                        "value": loaded_data.get("alternate_server_ip"),
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
            requests.patch(f"{loaded_data.get('discord_webhook_url')}/messages/{loaded_data['messageid']}", json=webhook_data)
            print("Status posted to Discord")
        except Exception as e:
            print(f"Failed to post to Discord: {e}")
        
        previous_status = status
        previous_response = response

    
    stop_event.wait(pollrateinseconds)

    

