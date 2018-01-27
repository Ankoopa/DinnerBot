# These are the dependencies.
import discord
import json
from discord.ext.commands import Bot
import http.client, urllib.request, urllib.parse, urllib.error
import search_google.api
import random

client = Bot(command_prefix="wtr-", pm_help = False)
subscription_key = '210e9b869f7249939d6c1cfc731f851d'
uri_base = 'westcentralus.api.cognitive.microsoft.com'

@client.event
async def on_ready():
    print ("Dinner Bot v0.1, ready to serve!")
    return await client.change_presence(game=discord.Game(name='Cooking Chicken'))

@client.event
async def on_message(message):
    try:
        if not message.author.bot:
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
                if img_txtinfo.count("WINNER") == 2 and 'CHICKEN' in img_txtinfo and 'DINNER' in img_txtinfo:
                    #await client.send_message(message.channel, "Congratulations, "+message.author.mention+"! Here's your chicken dinner: *insert pic*")
                    chicken_food = ['roasted chicken', 'fried chicken', 'chicken wings']
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
                    await client.send_message(message.channel, "Congratulations on ranking first, " + message.author.mention + "! Here's your chicken dinner: ", embed = e_img)
    except Exception as e:
        print (e)
        pass

client.run('NDA1NzEwNzY4OTc4NTI2MjA4.DUoXbA.YKgLUl9cqfgB5VqoAkAbCJKaRQI')
