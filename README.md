# Budget showpos

As a response to the CS:GO Update on 1.2.2022, which makes `cl_showpos` a cheat protected command, I have made a simple tool to display your position and angle in game.

![image](https://user-images.githubusercontent.com/73204452/152147297-bdb71c05-1f41-400f-a34d-ad803734550e.png)

## Controls

You can stop and resume the script by writing `!showpos` to the csgo console.

You can also bind this to a key for easier access:

    bind <key> "echo !showpos"

## Installation and setup

Add the following to the CS:GO launch options:

    -netconport 2121
    
Install python: https://www.python.org/downloads/
    
Clone and run the program:

    git clone https://github.com/Mikooboy/csgo_budget_showpos
    cd csgo_budget_showpos
    python main.py

Have fun!

-- Miko
