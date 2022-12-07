import traceback
import nextcord
import json
from nextcord.ext import commands, tasks
import config
import asyncio
import os


class error_correction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_correction_loop.start()

    @tasks.loop()
    async def error_correction_loop(self):
        while True:
            try:
                for filename in os.listdir('api'):
                    if filename.endswith('.json'):
                        _guildid = filename[:-5]
                        api_raw = open(f"api/{_guildid}.json")
                        api = json.load(api_raw)
                        state = api["general"][0]["state"]
                        int_state = int(state)
                        if int_state != 0:
                            if int_state != 1:
                                embed = nextcord.Embed(title=f"State error in {_guildid}",
                                                       description=f"```py\n State was set to {state}```")
                                error_log_channel = self.bot.get_channel(config.ERR_LOG_CHANNEL_ID)
                                await error_log_channel.send(embed=embed)
                                discord_id = api["general"][0]["discord_id"]
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
                        sender = api["general"][0]["sender"]
                        if sender != "discord":
                            if sender != "guilded":
                                embed = nextcord.Embed(title=f"Sender error in {_guildid}",
                                                       description=f"```py\n Sender was set to {sender}```")
                                error_log_channel = self.bot.get_channel(config.ERR_LOG_CHANNEL_ID)
                                await error_log_channel.send(embed=embed)
                                state_correction = api["general"][0]["state"]
                                discord_id = api["general"][0]["discord_id"]
                                guilded_id = api["general"][0]["guilded_id"]
                                discord_channel = api["general"][0]["discord_channel"]
                                guilded_channel = api["general"][0]["guilded_channel"]
                                data = {
                                    'general': [
                                        {
                                            'discord_id': f'{discord_id}',
                                            'guilded_id': f'{guilded_id}',
                                            'state': f'{state_correction}',
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
    bot.add_cog(error_correction(bot))
    print("[ Discord node ][ Guildcord - COG ] Started error-correction.")
