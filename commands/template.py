from twitchio.ext import commands

class Template(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Command Name')
    async def template(self, ctx):
        await ctx.send(f'Output')

def prepare(bot):
    bot.add_cog(Template(bot))
