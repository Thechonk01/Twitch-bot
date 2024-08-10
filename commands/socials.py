from twitchio.ext import commands

class Socials(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='discord')
    async def discord(self, ctx):
        """Get link to Discord server. Usage: !discord"""
        await ctx.send("Join my Discord server: discord.gg/sWkh39tAGe")

    @commands.command(name='socials')
    async def socials(self, ctx):
        """Get links to social media channels. Usage: !socials"""
        await ctx.send("Follow me on Twitter: https://x.com/Chonk_VAL")

def prepare(bot):
    bot.add_cog(Socials(bot))
