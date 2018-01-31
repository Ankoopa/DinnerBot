import discord
from modules import retrieve_stats

#pubg_api = core.PUBGAPI("390c0be4-4b0c-407c-bbf0-07426b9f6c66")
def get_stats(msgTxt):
    p_handle = msgTxt[len('~stats'):].lower().strip()
    if p_handle == '':
        e_msg = discord.Embed()
        e_msg.add_field(name="Usage of ~stats [*cmd*]:", value="*player_name*: See [*player_name*]'s stats.",
                        inline=False)
        return e_msg
    else:
        data = retrieve_stats.get_data(p_handle)
        labels = data[0]
        vals = data[1]
        e_msg = discord.Embed
        for i in labels:
            e_msg.add_field(name= i , value=vals[i.index(labels)])
        return e_msg