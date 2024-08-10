from twitchio.ext import commands

class Lurk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lurk')
    async def lurk(self, ctx):
        """Notify that you are lurking. Usage: !lurk"""
        await ctx.send(f"{ctx.author.name} is now lurking!")

    @commands.command(name='unlurk')
    async def unlurk(self, ctx):
        """Notify that you are back from lurking. Usage: !unlurk"""
        await ctx.send(f"{ctx.author.name} is back from lurking!")

def prepare(bot):
    bot.add_cog(Lurk(bot))
