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
    e_msg = discord.Embed().add_field(name="Changes:",
                                    value='Added stat tracking from Master PUBG. Use "w!stats *handle*" to see a '
                                          "player's stats", inline=False)
    for server in client.servers:
        channels = server.channels
        ch = discord.utils.get(channels, name='general', type=discord.ChannelType.text)
        print (ch)
        ch_id = client.get_channel(ch)
        print (ch_id)
        await client.send_message(ch, "WaiterBot has been updated to v0.5!", embed=e_msg)
    print ("Waiter Bot updated!")
    print ("Waiter Bot v0.5, ready to serve!")
    return await client.change_presence(game=discord.Game(name='Testing2'))

@client.event
async def on_message(message):
    try:
        if message.content.lower().startswith("w!stats"):
            msg = stat_tracker.get_stats(message.content)
            await client.send_message(message.channel, msg[1], embed=msg[0])
            return
        elif('.png') in str(message.attachments[0]) or ('.jpg') in str(message.attachments[0]):
            img = json.loads(json.dumps(message.attachments[0]))
            img_url = img['url']
            img_get = {'url': img_url}
            img_get2 = json.dumps(img_get)
            print (img_get2)

            headers = {
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': subscription_key,
            }
            params = urllib.parse.urlencode({
                'language': 'unk',
                'detectOrientation ': 'true',
            })
            conn = http.client.HTTPSConnection(uri_base)
            conn.request("POST", "/vision/v1.0/ocr?%s" % params, img_get2, headers)

            response = conn.getresponse()
            data = response.read()
            parsed = json.loads(data)

            print("Response:")
            print(json.dumps(parsed, sort_keys=True, indent=2))
            conn.close()

            img_txtinfo = str(parsed['regions'])
            print (img_txtinfo)
            win_txt = ['WINNER', 'CHICKEN', 'DINNER', 'EXIT', 'TO', 'LOBBY']
            def checkwin_img():
                chk = 0
                for i in win_txt:
                    if i in img_txtinfo:
                        chk += 1
                return chk
            print (checkwin_img())
            if checkwin_img() == 6:
                chicken_food = ['roasted chicken', 'fried chicken', 'chicken wings', 'chicken nuggets']
                buildargs = {
                    'serviceName': 'customsearch',
                    'version': 'v1',
                    'developerKey': 'AIzaSyCErN7v0GStDFah5P8rNyj4LvIQj0C8rMY'
                }
                cseargs = {
                    'q': random.choice(chicken_food),
                    'cx': '018188259780999380729:dscyf9jt_vm',
                    'searchType': 'image',
                    'imgType': 'photo',
                    'num': 10
                }
                results = search_google.api.results(buildargs, cseargs)
                links = results.links
                img_link = random.choice(links)
                e_img = discord.Embed()
                e_img = e_img.set_image(url = img_link)
                print(links)
                print(img_link)
                type(img_link)
                await client.send_message(message.channel, ":chicken: Congratulations on ranking first, " +
                        message.author.mention + "! Here's your chicken dinner: ", embed = e_img)
            return
    except Exception as e:
        print (e)
        traceback.print_exc()
    return

client.run('NDA2ODA3NzY5MjI5MDMzNTAz.DU4rFQ.Y__6zlIORmqqiKHO01CXOApPgBU')