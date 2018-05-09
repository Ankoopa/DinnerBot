import discord
import json
from discord.ext.commands import Bot
from modules import stat_tracker
import http.client, urllib.request, urllib.parse, urllib.error
import search_google.api
import random
import traceback

client = Bot(command_prefix="w!", pm_help = False)

subscription_key = '210e9b869f7249939d6c1cfc731f851d'
uri_base = 'westcentralus.api.cognitive.microsoft.com'

@client.event
async def on_ready():
    print ("Waiter Bot updated!")
    print ("Waiter Bot v0.7, ready to serve!")
    return await client.change_presence(game=discord.Game(name='w!stats'))

@client.event
async def on_message(message):
    try:
        if not message.attachments:
            if message.content.lower().startswith("w!stats"):
                msg = stat_tracker.get_stats(message.content)
                if len(msg) == 4:
                    await client.send_message(message.channel, msg[3], embed=msg[0])
                    await client.send_message(message.channel, embed=msg[1])
                    await client.send_message(message.channel, embed=msg[2])
                elif len(msg) == 3:
                    await client.send_message(message.channel, msg[2], embed=msg[0])
                    await client.send_message(message.channel, embed=msg[1])
                else:
                    await client.send_message(message.channel, msg[1], embed=msg[0])
                return
            elif message.content.lower().startswith("w!cmds"):
                e_msg = discord.Embed()
                e_msg.add_field(name="w!stats [region] [handle] ('recent'): ",
                                value="See a PUBG player's (recent) stats from a specifc region.\n\n"
                                      "Region codes:\n"
                                      "-SEA: Southeast Asia\n-AS: Asia\n-NA: North America\n"
                                      "-EU: Europe\n-OC: Oceania.",
                                inline=True)
                return await client.send_message(message.channel, "List of WaiterBot commands: ",embed=e_msg)
            return
    except Exception as e:
        traceback.print_exc()
    return

client.run('NDA1NzEwNzY4OTc4NTI2MjA4.DUoXbA.YKgLUl9cqfgB5VqoAkAbCJKaRQI')