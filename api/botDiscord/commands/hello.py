from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hello(self, message, args=[]):
        
        await message.reply(message.author.id)

    
def setup(client):
    client.add_cog(Hello(client))