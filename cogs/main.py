import os
import traceback
import nextcord
import json
from nextcord.ext import commands
from nextcord import application_command

client = commands.Bot(command_prefix=".", intents=nextcord.Intents.all())


class main(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @application_command.slash_command(name="register", description="Register your servers in the Guildcord "
                                                                    "API", default_member_permissions=536870928)
    async def register(self, interaction: nextcord.Interaction, guilded_guild_id, channel: nextcord.TextChannel, guilded_channel_id: str,
                       guilded_webhook_url: str, discord_mod_log_channel: nextcord.TextChannel, guilded_mod_log_channel_id: str):
        try:
            try:
                open(f"./api/{interaction.guild.id}.json", "x")
            except:
                pass
            try:
                f = open(f"./api/{interaction.guild.id}.json", "w")
                discord_webhook = await channel.create_webhook(name="Guildcord - Forwarding")
                discord_webhook_url = discord_webhook.url
                print(guilded_webhook_url)
                data = {
                    'general': [
                        {
                            'discord_id': f'{interaction.guild.id}',
                            'guilded_id': f'{guilded_guild_id}',
                            'state': '0',
                            'sender': None,
                            'receiver': '',
                            'discord_channel': f'{channel.id}',
                            'guilded_channel': f'{guilded_channel_id}',
                            'discord-webhook-url': discord_webhook_url,
                            'guilded-webhook-url': guilded_webhook_url,
                            'discord-mod-logs-channel-id': discord_mod_log_channel.id,
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
                                    "is-cdn": True,
                                    "attachments": [
                                        {
                                            "url": "https://raw.githubusercontent.com/Guildcord-API/api-main/main/logo.png"
                                        }
                                    ]
                                }
                        }
                    ]
                }
                json.dump(data, f)
                await interaction.response.send_message(":white_check_mark: - Registered this server successfully.",
                                                        ephemeral=True)
            except:
                await interaction.response.send_message(":x: - This server is already registered.",
                                                        ephemeral=True)
                traceback.print_exc()
        except:
            traceback.print_exc()

    @application_command.slash_command(name="api-data", description="Get the data of your server and group", default_member_permissions=8)
    async def getdata(self, interaction: nextcord.Interaction):
        try:
            data = open(f"./api/{interaction.guild.id}.json")
            for i in data:
                embed = nextcord.Embed(title="Your data", description=f"```json\n{i}```")
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            await interaction.response.send_message(":x: - We did not found any data belonging to this server.",
                                                    ephemeral=True)

    @application_command.slash_command(name="delete-server", description="Delete your servers in our API.", default_member_permissions=8)
    async def delete_server(self, interaction: nextcord.Interaction):
        try:
            cog = client.extensions.get(client.extensions, name="cogs.forward")
            client.unload_extension(cog)
            data = f"api/{interaction.guild.id}.json"
            os.remove(data)
            client.load_extension(cog)
            await interaction.response.send_message(":white_check_mark: - Your servers were successfully deleted.",
                                                    ephemeral=True)
        except:
            await interaction.response.send_message(":x: - We did not found any data of your servers.", ephemeral=True)
            traceback.print_exc()

    @application_command.slash_command(name="config", description="Edit your configuration in our API.", default_member_permissions=8)
    async def config(self, interaction: nextcord.Interaction, discord_id: int = None,
                     discord_channel: nextcord.TextChannel = None, guilded_id: str = None, guilded_channel: str = None):
        try:
            api_raw = open(f"../api/{interaction.guild.id}.json", "r+")
            api = json.load(api_raw)
            state = api["general"][0]["state"]
            if state == "1":
                await interaction.response.send_message(":x: - Your node has unforwarded messages.",
                                                        ephemeral=True)
            else:
                if discord_id and discord_channel and guilded_channel and guilded_id is None:
                    await interaction.response.send_message(":x: - Can't edit nothing.",
                                                            ephemeral=True)
                else:
                    api_raw.truncate(0)
                    if discord_id is not None:
                        api["general"][0]["discord_id"] = discord_id
                        json.dump(api, api_raw)
                        api_raw.close()
        except:
            await interaction.response.send_message(":x: - We couldn't find your API node.", ephemeral=True)
            traceback.print_exc()


def setup(bot):
    bot.add_cog(main(bot))
    print("[ Discord node ][ Guildcord - COG ] Started main.")
