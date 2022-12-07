import asyncio
import traceback
import nextcord
import json
from nextcord.ext import commands, tasks
import config
import os

client = commands.Bot(command_prefix=".", intents=nextcord.Intents.all())


class commiter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            for filename in os.listdir('api'):
                if filename.endswith('.json'):
                    _guildid = filename[:-5]
                    api_raw = open(f"api/{_guildid}.json")
                    api = json.load(api_raw)
                    discord_channel_check = api["general"][0]["discord_channel"]
                    if message.channel.id == int(discord_channel_check):
                        if message.author.id != self.bot.user.id:
                            discord_id = api["general"][0]["discord_id"]
                            guilded_id = api["general"][0]["guilded_id"]
                            discord_channel = api["general"][0]["discord_channel"]
                            guilded_channel = api["general"][0]["guilded_channel"]
                            data = {
                                'general': [
                                    {
                                        'discord_id': f'{discord_id}',
                                        'guilded_id': f'{guilded_id}',
                                        'state': '1',
                                        'sender': 'discord',
                                        'reciever': 'guilded',
                                        'discord_channel': f'{discord_channel}',
                                        'guilded_channel': f'{guilded_channel}',
                                    }
                                ],
                                'meta': [
                                    {
                                        'text': f'{message.content}',
                                        'sender': f'{message.author}',
                                    }
                                ]
                            }
                            api_raw.close()
                            f = open(f"api/{_guildid}.json", "w")
                            json.dump(data, f)
                            f.close()
                            await message.delete()
        except:
            pass
            traceback.print_exc()



def setup(bot):
    bot.add_cog(commiter(bot))
    print("[ Discord node ][ Guildcord - COG ] Started commiter.")
