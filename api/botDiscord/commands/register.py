from discord.ext import commands
import discord


reaction_roles_data = {}

class Register(commands.Cog):
    def __init__(self, client):
        self.client = client

    def parse_reaction_payload(self, payload: discord.RawReactionActionEvent):
        guild_id = payload.guild_id
        data = reaction_roles_data.get(str(guild_id), None)
        if data is not None:
            for rr in data:
                emote = rr.get("emote")
                if payload.message_id == rr.get("messageID"):
                    if payload.channel_id == rr.get("channelID"):
                        if str(payload.emoji) == emote:
                            guild = self.bot.get_guild(guild_id)
                            role = guild.get_role(rr.get("roleID"))
                            user = guild.get_member(payload.user_id)
                            return role, user
        return None, None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        print(payload.message_id)



    @commands.command()
    async def register(self, message, *args):
        def check(reaction, user):
            return True
        dm_channel = None
        if not message.author.dm_channel:
            dm_channel = await message.author.create_dm()
        else: 
            dm_channel = message.author.dm_channel

        embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
        embedVar.add_field(name="Field1", value="hi", inline=False)
        embedVar.add_field(name="Field2", value="hi2", inline=False)

        mens = await dm_channel.send(embed=embedVar)
        
        await mens.reply("Deu nada")
    
    @commands.command()
    async def meucord(self, message, *args):
        return
        
        

    
def setup(client):
    client.add_cog(Register(client))