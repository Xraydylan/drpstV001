import discord
import dropbox
import CONECT

client = discord.Client()

@client.event
async def on_ready():
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)

    f = open('name_info.txt', 'rb')

    dbx.files_upload(f.read(), "/test_txt.txt")

client.run(CONECT.TOKEN)