import asyncio
import traceback
import nextcord
import json
from nextcord.ext import commands, tasks
import config
import os

client = commands.Bot(command_prefix=".", intents=nextcord.Intents.all())


class forward(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forward_loop.start()

    @tasks.loop()
    async def forward_loop(self):
        while True:
            try:
                for filename in os.listdir('api'):
                    if filename.endswith('.json'):
                        _guildid = filename[:-5]
                        api_raw = open(f"api/{_guildid}.json")
                        api = json.load(api_raw)
                        state = api["general"][0]["state"]
                        sender = api["general"][0]["sender"]
                        reciever = api["general"][0]["reciever"]
                        if state == "1":
                            channel_id = api["general"][0]["discord_channel"]
                            discord_id = api["general"][0]["discord_id"]
                            guild = self.bot.get_guild(int(discord_id))
                            channel = nextcord.utils.get(guild.channels, id=int(channel_id))
                            text = api["meta"][0]["text"]
                            author = api["meta"][0]["sender"]
                            embed = nextcord.Embed(title=author, description=text)
                            if sender == "discord":
                                embed.set_footer(text="Sent from this server.")
                                await channel.send(embed=embed)
                            if reciever == "discord":
                                embed.set_footer(text="Sent from guilded server.")
                                await channel.send(embed=embed)
                            guilded_id = api["general"][0]["guilded_id"]
                            discord_channel = api["general"][0]["discord_channel"]
                            guilded_channel = api["general"][0]["guilded_channel"]
                            data = {
                                'general': [
                                    {
                                        'discord_id': f'{discord_id}',
                                        'guilded_id': f'{guilded_id}',
                                        'state': '0',
                                        'sender': '',
                                        'reciever': '',
                                        'discord_channel': f'{discord_channel}',
                                        'guilded_channel': f'{guilded_channel}',
                                    }
                                ],
                                'meta': [
                                    {
                                        'text': '',
                                        'sender': '',
                                    }
                                ]
                            }
                            api_raw.close()
                            f = open(f"api/{_guildid}.json", "w")
                            json.dump(data, f)
                            f.close()
            except:
                pass
                traceback.print_exc()
            await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(forward(bot))
    print("[ Discord node ][ Guildcord - COG ] Started forward.")
