import json
import os
from twitchio.ext import commands
from datetime import datetime, timedelta

class Viewtime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.viewtime_file = "viewtime.json"
        self.viewtime_data = self.load_viewtime_data()
        self.join_times = {}  # Track when users join

    def load_viewtime_data(self):
        """Load the viewtime data from a JSON file."""
        if os.path.exists(self.viewtime_file):
            with open(self.viewtime_file, 'r') as f:
                return json.load(f)
        return {}

    def save_viewtime_data(self):
        """Save the viewtime data to a JSON file."""
        with open(self.viewtime_file, 'w') as f:
            json.dump(self.viewtime_data, f, indent=4)

    def update_viewtime(self, username, minutes_watched):
        """Update the viewtime for a user."""
        self.viewtime_data[username] = self.viewtime_data.get(username, 0) + minutes_watched
        self.save_viewtime_data()

    @commands.command(name='watchtime')
    async def watchtime(self, ctx, username: str = None):
        if not username:
            username = ctx.author.name

        minutes = self.viewtime_data.get(username, 0)  # Default to 0 if user has no viewtime recorded
        hours, minutes = divmod(minutes, 60)
        await ctx.send(f"{username} has watched the stream for {hours} hours and {minutes} minutes.")

    @commands.Cog.event()
    async def event_ready(self):
        """An event triggered when the bot is ready."""
        print("Bot is ready!")

    @commands.Cog.event()
    async def event_join(self, channel, user):
        """An event triggered when a user joins the channel."""
        self.join_times[user.name] = datetime.utcnow()

    @commands.Cog.event()
    async def event_part(self, channel, user):
        """An event triggered when a user leaves the channel."""
        join_time = self.join_times.pop(user.name, None)
        if join_time:
            now = datetime.utcnow()
            elapsed_time = now - join_time
            minutes_watched = int(elapsed_time.total_seconds() // 60)
            self.update_viewtime(user.name, minutes_watched)

    @commands.Cog.event()
    async def event_message(self, message):
        """An event triggered for every message received by the bot."""
        # Just a fallback to ensure viewtime is calculated if the user sends a message before leaving
        if message.author.name in self.join_times:
            join_time = self.join_times[message.author.name]
            now = datetime.utcnow()
            elapsed_time = now - join_time
            if elapsed_time >= timedelta(minutes=1):
                minutes_watched = int(elapsed_time.total_seconds() // 60)
                self.update_viewtime(message.author.name, minutes_watched)
                self.join_times[message.author.name] = now

        await self.bot.handle_commands(message)

def prepare(bot):
    bot.add_cog(Viewtime(bot))
