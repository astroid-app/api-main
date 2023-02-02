import asyncio
import traceback
import nextcord
import json
from nextcord.ext import commands, tasks
import os
from nextcord import Webhook
import aiohttp

client = commands.Bot(command_prefix=".", intents=nextcord.Intents.all())


class forward(commands.Cog):
    def __init__(self, client):
        self.client = client
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
                        receiver = api["general"][0]["receiver"]
                        if state == "1":
                            if receiver == "discord":
                                author_id = api["meta"][0]["sender-id"]
                                text_log = api["meta"][0]["text"]
                                discord_mod_log_channel_id = api["general"][0]["discord-mod-logs-channel-id"]
                                guilded_mod_log_channel_id = api["general"][0]["guilded-mod-logs-channel-id"]
                                mod_log_channel = self.client.get_channel(discord_mod_log_channel_id)
                                embed = nextcord.Embed(title=f"New message from Guilded",
                                                       description=f"**User ID:** {author_id}\n"
                                                                   f"**Message:** `{text_log}`")
                                await mod_log_channel.send(embed=embed)
                                if api["meta"][0]["cdn"]["is-cdn"] is False:
                                    discord_id = api["general"][0]["discord_id"]
                                    text = api["meta"][0]["text"]
                                    author = api["meta"][0]["sender"]
                                    author_url = api["meta"][0]["author-profile"]
                                    webhook_url = api["general"][0]["discord-webhook-url"]
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
                                    guilded_id = api["general"][0]["guilded_id"]
                                    discord_channel = api["general"][0]["discord_channel"]
                                    guilded_channel = api["general"][0]["guilded_channel"]
                                    discord_webhook_url = api["general"][0]["discord-webhook-url"]
                                    guilded_webhook_url = api["general"][0]["guilded-webhook-url"]
                                    discord_mod_log_channel_id = api["general"][0]["discord-mod-logs-channel-id"]
                                    guilded_mod_log_channel_id = api["general"][0]["guilded-mod-logs-channel-id"]
                                    data = {
                                        'general': [
                                            {
                                                'discord_id': f'{discord_id}',
                                                'guilded_id': f'{guilded_id}',
                                                'state': '0',
                                                'sender': None,
                                                'receiver': '',
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
                                                'text': '',
                                                "author-profile": "",
                                                'sender': '',
                                                'sender-id': '',
                                                'cdn':
                                                    {
                                                        "is-cdn": False,
                                                        "attachments": [
                                                            {
                                                                "url": ""
                                                            }
                                                        ]
                                                    }
                                            }
                                        ]
                                    }
                                    api_raw.close()
                                    if receiver == "discord":
                                        f = open(f"api/{_guildid}.json", "w")
                                        json.dump(data, f)
                                        f.close()
                                elif api["meta"][0]["cdn"]["is-cdn"] is True:
                                    discord_id = api["general"][0]["discord_id"]
                                    guilded_id = api["general"][0]["guilded_id"]
                                    discord_channel = api["general"][0]["discord_channel"]
                                    guilded_channel = api["general"][0]["guilded_channel"]
                                    discord_webhook_url = api["general"][0]["discord-webhook-url"]
                                    guilded_webhook_url = api["general"][0]["guilded-webhook-url"]
                                    text = api["meta"][0]["text"]
                                    author = api["meta"][0]["sender"]
                                    author_url = api["meta"][0]["author-profile"]
                                    webhook_url = api["general"][0]["discord-webhook-url"]
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
                                    discord_mod_log_channel_id = api["general"][0]["discord-mod-logs-channel-id"]
                                    guilded_mod_log_channel_id = api["general"][0]["guilded-mod-logs-channel-id"]
                                    data = {
                                        'general': [
                                            {
                                                'discord_id': f'{discord_id}',
                                                'guilded_id': f'{guilded_id}',
                                                'state': '0',
                                                'sender': None,
                                                'receiver': '',
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
                                                'text': '',
                                                "author-profile": "",
                                                'sender': '',
                                                'sender-id': '',
                                                'cdn':
                                                    {
                                                        "is-cdn": False,
                                                        "attachments": [
                                                            {
                                                                "url": ""
                                                            }
                                                        ]
                                                    }
                                            }
                                        ]
                                    }

                                    api_raw.close()
                                    if receiver == "discord":
                                        f = open(f"api/{_guildid}.json", "w")
                                        json.dump(data, f)
                                        f.close()
            except:
                pass
                traceback.print_exc()
            await asyncio.sleep(1)


def setup(client):
    client.add_cog(forward(client))
    print("[ Discord node ][ Guildcord - COG ] Started forward.")
