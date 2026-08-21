# PZrconDicord
A simple Rcon to Discord webhook "Connecter", to Show server status, IP,Port and Players online
# Build

install dependencies
`python -m pip install requests rcon pathlib pyinstaller`

Build it using 
`pyisntaller --onefile Rcon.py`
# Setup
1. After first running the app/script it will close and make a savefile.json
2. Edit savefile.json with you Server details
3. run it again 
# Note
Leave "messageid" in savefile.json as it is, unless you know what you are doing or if you need to post status as new message then make it null

# Note 2 
might some more things like if you are running from server on lan and you want to show public ip in webhook i could separate the two.

maybe add some more things like command execution
