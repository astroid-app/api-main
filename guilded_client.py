import guilded
from guilded.ext import commands
import traceback
import asyncio
import os
import json
import config
from guilded import Webhook
import aiohttp

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("[ Guilded node ][ Guildcord - CLIENT ] Started Guilded client.")
    bot.loop.create_task(forward_loop())


async def forward_loop():
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
                        if receiver == "guilded":
                            author_id = api["meta"][0]["sender-id"]
                            text_log = api["meta"][0]["text"]
                            discord_mod_log_channel_id = api["general"][0]["discord-mod-logs-channel-id"]
                            guilded_mod_log_channel_id = api["general"][0]["guilded-mod-logs-channel-id"]
                            mod_log_channel = await bot.getch_channel(guilded_mod_log_channel_id)
                            embed = guilded.Embed(title=f"New message from Discord",
                                                   description=f"**User ID:** {author_id}\n"
                                                               f"**Message:** `{text_log}`")
                            await mod_log_channel.send(embed=embed)
                            if api["meta"][0]["cdn"]["is-cdn"] is False:
                                discord_id = api["general"][0]["discord_id"]
                                text = api["meta"][0]["text"]
                                author = api["meta"][0]["sender"]
                                author_url = api["meta"][0]["author-profile"]
                                webhook_url = api["general"][0]["guilded-webhook-url"]
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
                                if receiver == "guilded":
                                    f = open(f"api/{_guildid}.json", "w")
                                    json.dump(data, f)
                                    f.close()
                            elif api["meta"][0]["cdn"]["is-cdn"] is True:
                                discord_id = api["general"][0]["discord_id"]
                                text = api["meta"][0]["text"]
                                author = api["meta"][0]["sender"]
                                author_url = api["meta"][0]["author-profile"]
                                guilded_webhook_url = api["general"][0]["guilded-webhook-url"]
                                webhook_url = api["general"][0]["guilded-webhook-url"]
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
                                # attachment_url = api["meta"][0]["cdn"]["attachments"][0]["url"]
                                guilded_id = api["general"][0]["guilded_id"]
                                discord_channel = api["general"][0]["discord_channel"]
                                guilded_channel = api["general"][0]["guilded_channel"]
                                discord_webhook_url = api["general"][0]["discord-webhook-url"]
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
                                if receiver == "guilded":
                                    f = open(f"api/{_guildid}.json", "w")
                                    json.dump(data, f)
                                    f.close()

        except:
            pass
            traceback.print_exc()
        await asyncio.sleep(1)


@bot.event
async def on_message(message):
    try:
        for filename in os.listdir('api'):
            if filename.endswith('.json'):
                _guildid = filename[:-5]
                api_raw = open(f"api/{_guildid}.json")
                api = json.load(api_raw)
                guilded_channel_check = api["general"][0]["guilded_channel"]
                if message.channel.id == guilded_channel_check:
                    if message.author.id != bot.user.id:
                        if not message.webhook_id:
                            guilded_mod_log_channel_id = api["general"][0]["guilded-mod-logs-channel-id"]
                            mod_log_channel = await bot.getch_channel(guilded_mod_log_channel_id)
                            embed = guilded.Embed(title=f"New message from Guilded",
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
                                discord_mod_log_channel_id = api["general"][0]["discord-mod-logs-channel-id"]
                                data = {
                                    'general': [
                                        {
                                            'discord_id': f'{discord_id}',
                                            'guilded_id': f'{guilded_id}',
                                            'state': '1',
                                            'sender': 'guilded',
                                            'receiver': 'discord',
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
                                webhook_url = api_new["general"][0]["guilded-webhook-url"]
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
                                discord_mod_log_channel_id = api["general"][0]["discord-mod-logs-channel-id"]
                                guilded_mod_log_channel_id = api["general"][0]["guilded-mod-logs-channel-id"]
                                data = {
                                    'general': [
                                        {
                                            'discord_id': f'{discord_id}',
                                            'guilded_id': f'{guilded_id}',
                                            'state': '1',
                                            'sender': 'guilded',
                                            'receiver': 'discord',
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
                                webhook_url = api_new["general"][0]["guilded-webhook-url"]
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
        pass
        traceback.print_exc()


bot.run(config.GUILDED_TOKEN)
