import discord
import dropbox
import CONECT

client = discord.Client()

@client.event
async def on_ready():
    print("Ready")


    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)

    metadata, f = dbx.files_download('/' + "name.jpg")

    out = open("neu.jpg", 'wb')
    out.write(f.content)
    out.close()

    f = open('neu.txt', 'rb')

    dbx.files_upload(f.read(), "/Test1/neu.jpg")
    f.close()
client.run(CONECT.TOKEN)
