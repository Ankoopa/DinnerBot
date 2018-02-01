import discord
from modules import retrieve_stats

def get_stats(msgTxt):
    txt = None
    e_msg = discord.Embed()
    p_handle = msgTxt[len('w!stats'):].strip()
    if p_handle == '':
        e_msg.add_field(name="Usage of w!stats *command*:", value="*handle*: See the specified player's stats.",
                        inline=False)
        return e_msg, txt
    else:
        try:
            data = retrieve_stats.get_data(p_handle)
            labels = data[0]
            vals = data[1]
            labels = [e for e in labels if e not in {labels[8], labels[9]}]
            vals = [e for e in vals if e not in {vals[8], vals[9]}]
            print(labels)
            print(vals)
            for i in labels:
                ind = labels.index(i)
                e_msg.add_field(name=str(labels[ind])+":", value=str(vals[ind]), inline=True)
            e_msg.set_footer(text="Powered by masterpubg.com. To see more stats, go to: "
                                  "masterpubg.com/profile/"+p_handle)
            txt = "*"+p_handle + "*'s stats:"
            return e_msg, txt
        except Exception:
            e_msg.add_field(name="Reason: ", value="Unable to retrieve data for '*" + p_handle+"*'")
            txt = "An error has occurred in retrieving stats"
            return e_msg, txt