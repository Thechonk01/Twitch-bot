from twitchio.ext import commands

class CommandsList(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='command')
    async def command_usage(self, ctx, command_name: str = None):
        if not command_name:
            await ctx.send("Please provide a command name to get its usage. Example: !commands ban")
            return

        command = self.bot.get_command(command_name)

        if command is None:
            await ctx.send(f"Command '{command_name}' not found.")
            return

        usage = f"{ctx.prefix}{command.name}"
        if command.aliases:
            usage += f" (aliases: {', '.join(command.aliases)})"
        help_text = command._callback.__doc__
        if help_text:
            usage += f" - {help_text.strip()}"

        await ctx.send(usage)

def prepare(bot):
    bot.add_cog(CommandsList(bot))
