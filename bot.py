import datetime
import discord
from discord.ext.commands import Bot
import datetime
import asyncio
from discord.ext import commands

import logging
import aiohttp
from discord.ext import tasks
import time

logger = logging.getLogger('discord')
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="!")



@tasks.loop(minutes=8)                
async def post_status():
    await bot.wait_until_ready()
    try:
        async with aiohttp.ClientSession() as s:
            headers = {'Authorization': 'nitradotoken', 'Content-Type': 'application/json'}
            #game server #1
            async with s.get(f"https://api.nitrado.net/services/serverid/gameservers", headers=headers) as t:   
                d = await t.json()
                g1_status = d['data']['gameserver']['status']
                #g1_name = d['data']['gameserver']['query']['server_name']
                g1_slots = d['data']['gameserver']['slots']
                g1_players = d['data']['gameserver']['query']['player_current']
                g1_playercount = "{}/{}".format(g1_players, g1_slots)
                g1_boostcode = "sdfkjnsk"
            if g1_status == "started":
                status = "🟢"
            elif g1_status == "stopped":
                status = "🔴"
            else:
                status = "🟡"
            async with s.get(f"https://api.nitrado.net/services/serverid", headers=headers) as t:   
                d = await t.json()
                g1_timeleft = int(d['data']['service']['suspending_in'])            
            str_tm = str(datetime.timedelta(seconds=g1_timeleft))
            day = str_tm.split(',')[0]
            hour, minute, second = str_tm.split(',')[1].split(':')
            g1_timeleft = f'{day}{hour} hour'
            embed = discord.Embed(title="Nitrado Status", description=f"🟢 - Server is online\n🔴 - Server is offline\n🟡 - Server is restarting or Nitrado error", timestamp=datetime.datetime.utcnow(), color=0x2F3136)
            embed.add_field(name="SERVERNAME {}".format(status), value="Player Count: {}\nTime Remaining: {}".format(g1_playercount, g1_timeleft), inline=False)    
            #first to actually send to the channel, stop the bot commment lines 51 and 52 and add channel id and message id to line 54
            #channel = bot.get_channel(977361637986140190)
            #await channel.send(embed=embed)
            message = await bot.get_channel(channelid).fetch_message(messageid)
            await message.edit(embed = embed)
    except:
        pass

#starts the task
post_status.start()      





bot.run('BOTTOKENGOESHERE')
