import asyncio
import traceback
import nextcord
import json
from nextcord.ext import commands, tasks
import os

client = commands.Bot(command_prefix=".", intents=nextcord.Intents.all())


class commiter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            for filename in os.listdir('./api'):
                if filename.endswith('.json'):
                    _guildid = filename[:-5]
                    api_raw = open(f"api/{_guildid}.json")
                    api = json.load(api_raw)
                    discord_channel_check = api["general"][0]["discord_channel"]
                    if message.channel.id == int(discord_channel_check):
                        if message.author.id != self.bot.user.id:
                            if not message.webhook_id:
                                if message.attachments:
                                    discord_id = api["general"][0]["discord_id"]
                                    guilded_id = api["general"][0]["guilded_id"]
                                    discord_channel = api["general"][0]["discord_channel"]
                                    guilded_channel = api["general"][0]["guilded_channel"]
                                    discord_webhook_url = api["general"][0]["discord-webhook-url"]
                                    guilded_webhook_url = api["general"][0]["guilded-webhook-url"]
                                    data = {
                                        'general': [
                                            {
                                                'discord_id': f'{discord_id}',
                                                'guilded_id': f'{guilded_id}',
                                                'state': '1',
                                                'sender': 'discord',
                                                'receiver': 'guilded',
                                                'discord_channel': f'{discord_channel}',
                                                'guilded_channel': f'{guilded_channel}',
                                                'discord-webhook-url': discord_webhook_url,
                                                'guilded-webhook-url': guilded_webhook_url,
                                            }
                                        ],
                                        'meta': [
                                            {
                                                'text': f'{message.content}',
                                                "author-profile": message.author.avatar.url,
                                                'sender': f'{message.author}',
                                                'cdn':
                                                    {
                                                        "is-cdn": True,
                                                        "attachments": [
                                                            {
                                                                "url": message.attachments[0].url
                                                            }
                                                        ]
                                                    }
                                            }
                                        ]
                                    }
                                    api_raw.close()
                                    f = open(f"api/{_guildid}.json", "w")
                                    json.dump(data, f)
                                    f.close()
                                    await message.delete()
                                else:
                                    discord_id = api["general"][0]["discord_id"]
                                    guilded_id = api["general"][0]["guilded_id"]
                                    discord_channel = api["general"][0]["discord_channel"]
                                    guilded_channel = api["general"][0]["guilded_channel"]
                                    discord_webhook_url = api["general"][0]["discord-webhook-url"]
                                    guilded_webhook_url = api["general"][0]["guilded-webhook-url"]
                                    data = {
                                        'general': [
                                            {
                                                'discord_id': f'{discord_id}',
                                                'guilded_id': f'{guilded_id}',
                                                'state': '1',
                                                'sender': 'discord',
                                                'receiver': 'guilded',
                                                'discord_channel': f'{discord_channel}',
                                                'guilded_channel': f'{guilded_channel}',
                                                'discord-webhook-url': discord_webhook_url,
                                                'guilded-webhook-url': guilded_webhook_url,
                                            }
                                        ],
                                        'meta': [
                                            {
                                                'text': f'{message.content}',
                                                "author-profile": message.author.avatar.url,
                                                'sender': f'{message.author}',
                                                'cdn':
                                                    {
                                                        "is-cdn": False,
                                                        "attachments": [
                                                            {
                                                                "url": "https://raw.githubusercontent.com/Guildcord-API/api-main/main/logo.png"
                                                            }
                                                        ]
                                                    }
                                            }
                                        ]
                                    }
                                    api_raw.close()
                                    f = open(f"api/{_guildid}.json", "w")
                                    json.dump(data, f)
                                    f.close()
                                    await message.delete()
        except:
            traceback.print_exc()



def setup(bot):
    bot.add_cog(commiter(bot))
    print("[ Discord node ][ Guildcord - COG ] Started commiter.")
