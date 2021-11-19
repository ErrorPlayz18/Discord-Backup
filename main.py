#Backup ur frnds nd servers in just one cmd
import discord
from discord.ext import commands
import discum
import os
import requests
import asyncio
import random
import codecs

token = ""

prefix = "-"
os.system('clear')

client = commands.Bot(command_prefix=prefix, self_bot = True)

intents = discord.Intents.all()
intents.members = True

def check_token():
    if requests.get("https://discord.com/api/v8/users/@me", headers={"Authorization": f'{token}'}).status_code == 200:
        return "user"
    else:
        return "bot"



@client.event
async def on_ready():
  print(f"Successfully Logged Into {client.user}")



@client.command(aliases=["friendbackup"])
async def backupfriends(ctx):
        print("Backup Initiated...")
        request = requests.get("https://discord.com/api/v6/users/@me/relationships", headers={"authorization": token})
        json = request.json()
        ids = []
        blockedIds = []
        incoming = []
        outgoing = []
        for item in json:
            if item["type"] == 1:
                print(f'Backed up {str(item["user"]["username"]) + "#" + str(item["user"]["discriminator"])}!')             
                ids.append(
                    str(item["id"]) + 
                    " : " + 
                    str(item["user"]["username"]) + 
                    "#" + str(item["user"]["discriminator"])
                    )
            if item["type"] == 2:
                print(f'Backed up a blocked user : {str(item["user"]["username"]) + "#" + str(item["user"]["discriminator"])}')
                blockedIds.append(
                    str(item["id"]) + 
                    " : " + 
                    str(item["user"]["username"]) + 
                    "#" + str(item["user"]["discriminator"])
                    )
            if item["type"] == 3:
                print(f'Backed up an incoming friend request : {str(item["user"]["username"]) + "#" + str(item["user"]["discriminator"])}')
                incoming.append(
                    str(item["id"]) + 
                    " : " + 
                    str(item["user"]["username"]) + 
                    "#" + str(item["user"]["discriminator"])
                    )   
            if item["type"] == 4:
                print(f'Backed up an outgoing friend request : {str(item["user"]["username"]) + "#" + str(item["user"]["discriminator"])}')
                outgoing.append(
                    str(item["id"]) + 
                    " : " + 
                    str(item["user"]["username"]) + 
                    "#" + str(item["user"]["discriminator"])
                    ) 

        print("Backed up all friends....")
        await ctx.send(f"Successfully Backuped `{len(ids)}` friends, `{len(blockedIds)}` blocked, `{len(outgoing)}` Outgoing friend requests and `{len(incoming)}` Incoming friend requests to __data/friends.txt__.")

        if not ids:
            ids.append("Unable to find any friends...")
        if not blockedIds:
            blockedIds.append("Unable to find any blocked users...")
        if not outgoing:
            outgoing.append("Unable to find any outgoing friend requests...")
        if not incoming:
            incoming.append("Unable to find any incoming friend requests...")
                                                
        file = codecs.open("data/friends.txt", "w", encoding="utf-8")
        file.write(
            "Current Friends\n===============\n" + "\n".join(ids) + 
            "\n \nOutgoing Requests\n=================\n" + "\n".join(outgoing) + 
            "\n \nIncoming Requests\n=================\n" + "\n".join(incoming) + 
            "\n \nBlocked Users\n=============\n" + "\n".join(blockedIds)
            )
        file.close()




@client.command(aliases=["backupguilds", "serverbackup", "guildbackup"])
async def backupservers(ctx):
        DiscumClient = discum.Client(token=token,user_agent=get_random_user_agent())
        try:
            await ctx.message.delete()
        except:
            pass
        print("Server Backup Initiated!!!")
        guilds = requests.get("https://discordapp.com/api/v6/users/@me/guilds", headers={"authorization": token}).json()
        print("Searching all the guilds...")
        guildsIdsAndInvites = []
        for item in guilds:
            guildid = item["id"]
            guildname = item["name"]
            invite = ""

            print(f"Created guild inv for... {guildname}")
            server = discord.utils.get(client.guilds, id=int(guildid))
            for channel in server.text_channels:
                if invite == "":
                    invite = DiscumClient.createInvite(str(channel.id))
                    if invite.status_code == 200:
                        invite = invite.json()["code"]
                    else:
                        invite = ""
                    break

            if invite == "":
                invite = "Failed to create an invite."
            guildsIdsAndInvites.append(item["name"] + " : " + str(item["id"]) + " : discord.gg/" + str(invite))
            await asyncio.sleep(4)
        print(f"Successfully Saved all guilds data...")
        file = codecs.open("data/servers.txt", "w", encoding="utf-8")
        file.write("\n".join(guildsIdsAndInvites))
        file.close()        
        await ctx.send("Successfully Saved all guild data in __data/servers.txt__.")


# random user agent
def get_random_user_agent():
    userAgents = [
        "Mozilla/5.0 (Windows NT 6.2;en-US) AppleWebKit/537.32.36 (KHTML, live Gecko) Chrome/56.0.3075.83 Safari/537.32",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.1",
        "Mozilla/5.0 (Windows NT 8.0; WOW64) AppleWebKit/536.24 (KHTML, like Gecko) Chrome/32.0.2019.89 Safari/536.24",
        "Mozilla/5.0 (Windows NT 5.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.41 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3058.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3258.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2599.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.35 (KHTML, like Gecko) Chrome/27.0.1453.0 Safari/537.35",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.139 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/6.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.0.9757 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3258.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/6.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.1",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2151.2 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1204.0 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/67.0.3387.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.0.9757 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3359.181 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3251.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538 (KHTML, like Gecko) Chrome/36 Safari/538",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.18 Safari/535.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.355.0 Safari/533.3",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.4 Safari/532.0",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.35 (KHTML, like Gecko) Chrome/27.0.1453.0 Safari/537.35",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3359.181 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3057.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.14",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36 TC2",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3058.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3258.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2531.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36,gzip(gfe)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2264.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.29 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.150 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.14",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2714.0 Safari/537.36",
        "24.0.1284.0.0 (Windows NT 5.1) AppleWebKit/534.0 (KHTML, like Gecko) Chrome/24.0.1284.0.3.742.3 Safari/534.3",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1864.6 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Chrome/36.0.1985.125 CrossBrowser/36.0.1985.138 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Avast/70.0.917.102",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1615.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.14",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/6.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3608.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3251.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/54.2.133 Chrome/48.2.2564.133 Safari/537.36",
        "24.0.1284.0.0 (Windows NT 5.1) AppleWebKit/534.0 (KHTML, like Gecko) Chrome/24.0.1284.0.3.742.3 Safari/534.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/54.2.133 Chrome/48.2.2564.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/54.2.133 Chrome/48.2.2564.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.18 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2427.7 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.61 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Chrome/36.0.1985.125 CrossBrowser/36.0.1985.138 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/530.6 (KHTML, like Gecko) Chrome/2.0.174.0 Safari/530.6",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.29 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.104 Safari/537.36",
        "24.0.1284.0.0 (Windows NT 5.1) AppleWebKit/534.0 (KHTML, like Gecko) Chrome/24.0.1284.0.3.742.3 Safari/534.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Web Preview) Chrome/27.0.1453 Safari/537.36,gzip(gfe)",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.29 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.45 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.45",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.150 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2419.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Chrome/36.0.1985.125 CrossBrowser/36.0.1985.138 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1204.0 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2700.0 Safari/537.36#",
        "Mozilla/5.0 (Windows NT 10.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.16 (KHTML, like Gecko) Chrome/5.0.335.0 Safari/533.16",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.68 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.43 Safari/535.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2700.0 Safari/537.36#",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.114 Safari/537.36",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/530.6 (KHTML, like Gecko) Chrome/2.0.174.0 Safari/530.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538 (KHTML, like Gecko) Chrome/36 Safari/538",
        "Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.43 Safari/535.1",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.18 Safari/535.1",
        "Mozilla/5.0 (X11; Linux x86_64; 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/17.0.1410.63 Safari/537.31",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2583.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2151.2 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.18 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/536.36 (KHTML, like Gecko) Chrome/67.2.3.4 Safari/536.36",
        "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.172.0 Safari/530.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.69 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.81 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Safari/537.36 EdgA/41.0.0.1662",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.1"
    ]
    userAgent = random.choice(userAgents)
    return userAgent





client.run(token, bot=False)