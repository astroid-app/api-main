import traceback
import nextcord
from nextcord.ext import commands
import config
import asyncio
import os

client = commands.Bot(command_prefix=".", intents=nextcord.Intents.all())


@client.event
async def on_ready():
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            try:
                client.load_extension(f'cogs.{filename[:-3]}')
            except:
                traceback.print_exc()
    client.loop.create_task(change_presence())
    client.loop.create_task(sync_commands())


async def sync_commands():
    while True:
        await client.sync_application_commands()
        await asyncio.sleep(1)


async def change_presence():
    await client.change_presence(
        activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Your Guilded Server"))
    await asyncio.sleep(30)
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Guildcord API"))
    await asyncio.sleep(30)


client.run(config.DISCORD_TOKEN)
