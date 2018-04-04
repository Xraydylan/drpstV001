import dropbox
from dropbox.files import WriteMode
import discord
import CONECT
import os
import random


async def ex(args, message, client, invoke, server):
    print("Drop")
    dbx = dropbox.Dropbox(CONECT.DROP_TOKEN)
    if exist_all_folders(dbx,"/Pictures") == 4:
        if len(args) > 0:
            args_out = args.__str__()[1:-1].replace("'", "").replace(",", "")
            if args_out == "update":
                print("UPDATING")
                await update(dbx,client,message.channel)
            elif args_out == "reset info":
                await reset_info(dbx,client,message.channel)
            elif args_out == "send":
                await send(dbx,client,message.channel)
    else:
        await client.send_message(message.channel, "There is a storage problem. Folders are missing!")



def exist_all_folders(dbx, path):
    res = dbx.files_list_folder(path)
    count = 0
    for file in res.entries:
        count += 1
    return count


async def update(dbx,client,channel):
    if exist_all_folders(dbx,"/Pictures/input") > 0:
        await update_prcess(dbx,client,channel)
    else:
        await client.send_message(channel, "No new files in input.")

async def update_prcess(dbx,client,channel):
    await client.send_message(channel, "**Starting update**")
    await client.send_message(channel, "Update Status:")
    res = dbx.files_list_folder("/Pictures/input")
    count1 = 0.0
    for file in res.entries:
        count1 += 1.0

    count2 = 0.0
    count3 = 0.0
    for file in res.entries:

        metadata, f = dbx.files_download('/Pictures/input/' + file.name)

        name = get_name(dbx, file.name)

        savepath = "data/temp/"+name

        out = open(savepath, 'wb')
        out.write(f.content)
        out.close()

        pathdrop = "/Pictures/main/"+name
        up = open(savepath, 'rb')
        dbx.files_upload(up.read(), pathdrop, mode=WriteMode('overwrite'))
        up.close()
        os.remove("data/temp/"+name)
        dbx.files_delete_v2('/Pictures/input/' + file.name)
        #print (count1)
        #print(count2)
        #print(count3)
        #print("----")
        if (count2/count1)*100 >= count3:
            while (count2/count1)*100 > count3:
                count3 += 5
            await client.send_message(channel, "Over %s %s" % (str(count3),"%"))
        count2 += 1.0
    await client.send_message(channel, "Update Complete!!!")


def get_name(dbx, name):
    f_split = name.split(".")
    ending = len(f_split)-1
    f_type = f_split[ending]
    lastn = get_add_last_number(dbx)
    new_name = str(lastn) + "." + f_type
    return new_name



def get_add_last_number(dbx):
    metadata, f = dbx.files_download('/' + "Pictures/info/name_info.txt")
    numbers = str(f.content).replace("b", "").replace("'", "").split("\\r\\n")
    lastn = int(numbers[len(numbers)-1])+1
    out = open("data/info.txt", 'wb')
    out.write(f.content)
    out.close()
    txt = open("data/info.txt", 'w')
    txt.write(str(lastn))
    txt.close()
    up = open("data/info.txt", 'rb')
    dbx.files_upload(up.read(), "/Pictures/info/name_info.txt", mode=WriteMode('overwrite'))
    up.close()
    os.remove("data/info.txt")
    return lastn

async def reset_info(dbx,client,channel):
    await client.send_message(channel, "Info reseted")
    metadata, f = dbx.files_download('/' + "Pictures/info/name_info_reset.txt")
    out = open("data/info_reset.txt", 'wb')
    out.write(f.content)
    out.close()
    up = open("data/info_reset.txt", 'rb')
    dbx.files_upload(up.read(), "/Pictures/info/name_info.txt", mode=WriteMode('overwrite'))
    up.close()
    os.remove("data/info_reset.txt")

async def send(dbx,client,channel):
    res = dbx.files_list_folder("/Pictures/main")
    file_list = []
    for file in res.entries:
        file_list.append(file.name)

    if len(file_list) > 0:

        send_name = random.choice(file_list)

        metadata, f = dbx.files_download('/Pictures/main/' + send_name)

        savepath = "data/temp/" + send_name
        out = open(savepath, 'wb')
        out.write(f.content)
        out.close()

        await client.send_file(channel, savepath)

        pathdrop = "/Pictures/output/" + send_name
        up = open(savepath, 'rb')
        dbx.files_upload(up.read(), pathdrop, mode=WriteMode('overwrite'))
        up.close()

        dbx.files_delete_v2('/Pictures/main/' + send_name)
        os.remove("data/temp/"+send_name)
    else:
        print ("Empty")