import asyncio
import traceback
import nextcord
import json
from nextcord.ext import commands, tasks
import os
import aiohttp
from nextcord import Webhook

client = commands.Bot(command_prefix=".", intents=nextcord.Intents.all())


class commiter(commands.Cog):
    def __init__(self, client):
        self.client = client

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
                        if not message.author.bot:
                            if not message.webhook_id:
                                discord_mod_log_channel_id = api["general"][0]["discord-mod-logs-channel-id"]
                                guilded_mod_log_channel_id = api["general"][0]["guilded-mod-logs-channel-id"]
                                mod_log_channel = self.client.get_channel(discord_mod_log_channel_id)
                                embed = nextcord.Embed(title=f"New message from Discord",
                                                       description=f"**User ID:** {message.author.id}\n"
                                                                   f"**Message:** `{message.content}`")
                                await mod_log_channel.send(embed=embed)
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
                                                'discord-mod-logs-channel-id': discord_mod_log_channel_id,
                                                'guilded-mod-logs-channel-id': guilded_mod_log_channel_id,
                                            }
                                        ],
                                        'meta': [
                                            {
                                                'text': f'{message.content}',
                                                "author-profile": message.author.avatar.url,
                                                'sender': f'{message.author}',
                                                'sender-id': message.author.id,
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
                                    api_file = open(f"api/{_guildid}.json", "r")
                                    api_new = json.load(api_file)
                                    text = api_new["meta"][0]["text"]
                                    author = api_new["meta"][0]["sender"]
                                    author_url = api_new["meta"][0]["author-profile"]
                                    # attachment_url = api_new["meta"][0]["cdn"]["attachments"][0]["url"]
                                    webhook_url = api_new["general"][0]["discord-webhook-url"]
                                    session = aiohttp.ClientSession()
                                    webhook = Webhook.from_url(url=webhook_url, session=session)
                                    try:
                                        await webhook.send(text, avatar_url=author_url, username=author)
                                    except:
                                        await webhook.send(text, avatar_url=author_url,
                                                           username="(Guildcord) Invalid Name")
                                    finally:
                                        await session.close()
                                        if session.closed:
                                            print("session closed")
                                        else:
                                            print("couldn't close session")
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
                                                'discord-mod-logs-channel-id': discord_mod_log_channel_id,
                                                'guilded-mod-logs-channel-id': guilded_mod_log_channel_id,
                                            }
                                        ],
                                        'meta': [
                                            {
                                                'text': f'{message.content}',
                                                "author-profile": message.author.avatar.url,
                                                'sender': f'{message.author}',
                                                'sender-id': message.author.id,
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
                                    api_file = open(f"api/{_guildid}.json", "r")
                                    api_new = json.load(api_file)
                                    text = api_new["meta"][0]["text"]
                                    author = api_new["meta"][0]["sender"]
                                    author_url = api_new["meta"][0]["author-profile"]
                                    # attachment_url = api_new["meta"][0]["cdn"]["attachments"][0]["url"]
                                    webhook_url = api_new["general"][0]["discord-webhook-url"]
                                    session = aiohttp.ClientSession()
                                    webhook = Webhook.from_url(url=webhook_url, session=session)
                                    try:
                                        await webhook.send(text, avatar_url=author_url, username=author)
                                    except:
                                        await webhook.send(text, avatar_url=author_url,
                                                           username="(Guildcord) Invalid Name")
                                    finally:
                                        await session.close()
                                        if session.closed:
                                            print("session closed")
                                        else:
                                            print("couldn't close session")

        except:
            traceback.print_exc()



def setup(client):
    client.add_cog(commiter(client))
    print("[ Discord node ][ Guildcord - COG ] Started commiter.")
