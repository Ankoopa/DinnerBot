import discord
import json
from discord.ext.commands import Bot
import http.client, urllib.request, urllib.parse, urllib.error
import search_google.api
import random
from pypubg import core
import time

client = Bot(command_prefix="~", pm_help = False)
pubg_api = core.PUBGAPI("390c0be4-4b0c-407c-bbf0-07426b9f6c66")

subscription_key = '210e9b869f7249939d6c1cfc731f851d'
uri_base = 'westcentralus.api.cognitive.microsoft.com'

@client.event
async def on_ready():
    print ("Dinner Bot updated!")
    await client.change_presence(game=discord.Game(name='Updating...'))
    time.sleep(2)
    print ("Dinner Bot v0.1, ready to serve!")
    return await client.change_presence(game=discord.Game(name='Testing'))

@client.event
async def on_message(message):
    try:
        if('.png') in str(message.attachments[0]) or ('.jpg') in str(message.attachments[0]):
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
                await client.send_message(message.channel, "Congratulations on ranking first, " +
                        message.author.mention + "! Here's your chicken dinner: ", embed = e_img)
        return
    except Exception as e:
        print (e)
        pass
    return

@client.event
async def on_message(message):
    if message.content.lower().startswith("~stats"):
        p_handle = message.content[len('~stats'):].lower().strip()
        print(p_handle)
        if p_handle == '':
            await client.send_message(message.channel, "USAGE: '~stats [*your name*]'")
            return
        p_inf = pubg_api.player(p_handle)
        print (p_inf)
        if 'error' in p_inf:
            await client.send_message(message.channel, "Unable to retrieve stats.")
            await client.send_message(message.channel, "Reason: "+p_inf['error'])
        else:
            for sts in p_inf:
                await client.send_message(message.channel, "Here are "+p_handle+"'s stats.", embed=p_inf)
                await client.send_message(message.channel, "Powered by: ")
    return

client.run('NDA1NzEwNzY4OTc4NTI2MjA4.DUoXbA.YKgLUl9cqfgB5VqoAkAbCJKaRQI')
