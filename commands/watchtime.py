from twitchio.ext import commands
from datetime import datetime, timedelta
import json
import os

class Watchtime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.viewtime_file = "viewtime.json"
        self.viewtime_data = self.load_viewtime_data()
        self.join_times = {}  # Track when users join

    def load_viewtime_data(self):
        if os.path.exists(self.viewtime_file):
            with open(self.viewtime_file, 'r') as f:
                return json.load(f)
        return {}

    def save_viewtime_data(self):
        with open(self.viewtime_file, 'w') as f:
            json.dump(self.viewtime_data, f, indent=4)

    def update_viewtime(self, username, minutes_watched):
        self.viewtime_data[username] = self.viewtime_data.get(username, 0) + minutes_watched
        self.save_viewtime_data()

    @commands.command(name='watchtime')
    async def viewtime(self, ctx, username: str = None):
        if not username:
            username = ctx.author.name

        minutes = self.viewtime_data.get(username, 0)
        hours, minutes = divmod(minutes, 60)
        await ctx.send(f"{username} has watched the stream for {hours} hours and {minutes} minutes.")

    @commands.Cog.event()
    async def event_join(self, channel, user):
        self.join_times[user.name] = datetime.utcnow()

    @commands.Cog.event()
    async def event_part(self, channel, user):
        join_time = self.join_times.pop(user.name, None)
        if join_time:
            now = datetime.utcnow()
            elapsed_time = now - join_time
            minutes_watched = int(elapsed_time.total_seconds() // 60)
            self.update_viewtime(user.name, minutes_watched)

    @commands.Cog.event()
    async def event_message(self, message):
        if message.author is None or message.author.name == self.bot.nick:
            return

        # Process viewtime updates without invoking commands here
        username = message.author.name

        if username in self.join_times:
            join_time = self.join_times[username]
            now = datetime.utcnow()
            elapsed_time = now - join_time
            if elapsed_time >= timedelta(minutes=1):
                minutes_watched = int(elapsed_time.total_seconds() // 60)
                self.update_viewtime(username, minutes_watched)
                self.join_times[username] = now

        # Only process commands once, handled elsewhere
        # Removed: await self.bot.handle_commands(message)

def prepare(bot):
    bot.add_cog(Watchtime(bot))
