import os
import requests
from twitchio.ext import commands

class Raid(commands.Cog):

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

    @commands.command(name='raid')
    async def start_raid(self, ctx, target_channel: str):
        """Start a raid to another channel. Usage: !raid <target_channel>"""
        if ctx.author.is_mod:
            target_id = self.get_user_id(target_channel)
            if target_id:
                url = f"https://api.twitch.tv/helix/raids"
                data = {
                    "from_broadcaster_id": self.broadcaster_id,
                    "to_broadcaster_id": target_id
                }
                response = requests.post(url, headers=self.get_headers(), json=data)
                if response.status_code == 200:
                    await ctx.send(f"Raid started! Raiding {target_channel} now.")
                else:
                    await ctx.send(f"Failed to start raid. API returned {response.status_code}: {response.json().get('message')}")
            else:
                await ctx.send(f"User {target_channel} not found.")
        else:
            await ctx.send("You do not have permission to use this command.")

def prepare(bot):
    bot.add_cog(Raid(bot))
