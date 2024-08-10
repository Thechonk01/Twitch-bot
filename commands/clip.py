import os
import requests
from twitchio.ext import commands

class Clip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = os.getenv('TWITCH_OAUTH_TOKEN').split(':')[1]  # Extract token without 'oauth:' prefix
        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.broadcaster_id = self.get_user_id(os.getenv('TWITCH_CHANNEL'))

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Client-Id': self.client_id,
            'Content-Type': 'application/json'
        }

    def get_user_id(self, username):
        url = f"https://api.twitch.tv/helix/users?login={username}"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200 and response.json()['data']:
            return response.json()['data'][0]['id']
        return None

    @commands.command(name='clip')
    async def create_clip(self, ctx):
        """Create a clip from the current stream. Usage: !clip"""
        if ctx.author.is_mod:
            url = f"https://api.twitch.tv/helix/clips?broadcaster_id={self.broadcaster_id}"
            response = requests.post(url, headers=self.get_headers())
            if response.status_code == 202:
                clip_data = response.json()['data'][0]
                clip_url = f"https://clips.twitch.tv/{clip_data['id']}"
                await ctx.send(f"Clip created! Watch it here: {clip_url}")
            else:
                await ctx.send(f"Failed to create clip. API returned {response.status_code}: {response.json().get('message')}")
        else:
            await ctx.send("You do not have permission to use this command.")

def prepare(bot):
    bot.add_cog(Clip(bot))
