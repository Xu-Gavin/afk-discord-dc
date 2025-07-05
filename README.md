# AFK Discord Disconnect Utility
Disconnect from Discord after a specified amount of seconds

## Discord Settings Setup
In Discord settings, create a keybind and set "Disconnect From Voice Channel" to `]+[`.

![Discord Settings Image](assets/discord.png)

## To Build
Use `pyinstaller` to build: 
```
pyinstaller --windowed --icon=assets/icon.png --onefile --add-data "assets/icon.png;assets" afk-discord-dc.py
```
