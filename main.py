import discord
from discord import Game, Embed
from os import path
import CONECT
import STATICS
from use import use,get

from commands import cmd_new

client = discord.Client()
n_server = None

commands = {

    "new": cmd_new,
}


@client.event
async def on_ready():
    global n_server
    print("Bot is logged in successfully. Running on servers:\n")
    for s in client.servers:
        print("  - %s (%s)" % (s.name, s.id))
        if str(s.id) == CONECT.SERVER_ID:
            n_server = s
            print(n_server.name)
    if n_server == None:
        print("No matching server found!")

@client.event
async def on_message(message):
    global n_server
    if message.content.startswith(STATICS.PREFIX):
        invoke = message.content[len(STATICS.PREFIX):].split(" ")[0]
        args = message.content.split(" ")[1:]
        if commands.__contains__(invoke):
            await commands.get(invoke).ex(args, message, client, invoke, n_server)

client.run(CONECT.TOKEN)