# PZrconDiscord
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

use alternate ip to show alternate public on webhook incase you are access server on lan, serverip should lan ip and alternate ip should public ip of server

can run commands on server just type the command and press enter  

# Note 2 
~~might add some more things, like if you are running from server on lan and you want to show public ip in webhook that is different from the ip you are susing to access the server, i could separate the two.~~

~~maybe add some more things like command execution~~
done 

