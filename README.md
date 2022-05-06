# discord-bot-python
A bot to open and close (minecraft) servers.

## Dependencies
python-dotenv
discord.py

## Installation

In the root folder of the bot, create a file named `.env` containing the following:

```
DISCORD_TOKEN=<the token needed to use the discord API>
ADMIN=<your discord ID>
SERVER_TYPE_DIR=<server directory>
```

The folder containing the server also needs a named pipe `pipe.str` and a file `runserver` that reads commands sent by the bot from the pipe.
Why not send the commands directly to the server? Because then you can restart the bot and keep sending commands like nothing ever happened.

## Commands available

+ **svr help**: Shows some of the commands available
+ **svr status**: Show the status of all servers
+ **svr start [type]**: Starts the specified server. Needs privileges.
+ **svr stop [type]**: Stops the specified server. Needs privileges.
+ **svr pu [add|remove|check] [user] [type]**: Gives/Revokes/Checks privileges to open and close the specified server.
  If type is **operator**, the user will be able to give privileges to other users. Only the admin can give operator privileges. 
+ **svr shut**: Shuts down the bot.
