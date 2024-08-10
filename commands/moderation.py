import os
import requests
from twitchio.ext import commands

class Moderation(commands.Cog):

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

    @commands.command(name='ban')
    async def ban_user(self, ctx, user: str):
        """Ban a user from the channel. Usage: !ban <username>"""
        if ctx.author.is_mod:
            user_id = self.get_user_id(user)
            if user_id:
                url = f"https://api.twitch.tv/helix/moderation/bans?broadcaster_id={self.broadcaster_id}&moderator_id={self.broadcaster_id}"
                data = {
                    "data": {
                        "user_id": user_id,
                        "reason": "No reason provided"  # You can customize the reason
                    }
                }
                response = requests.post(url, headers=self.get_headers(), json=data)
                if response.status_code == 200:
                    await ctx.send(f"{user} has been banned.")
                else:
                    await ctx.send(f"Failed to ban {user}. API returned {response.status_code}: {response.json().get('message')}")
            else:
                await ctx.send(f"User {user} not found.")
        else:
            await ctx.send("You do not have permission to use this command.")

    @commands.command(name='timeout')
    async def timeout_user(self, ctx, user: str, duration: int):
        """Timeout a user from the channel. Usage: !timeout <username> <duration_in_seconds>"""
        if ctx.author.is_mod:
            user_id = self.get_user_id(user)
            if user_id:
                url = f"https://api.twitch.tv/helix/moderation/bans?broadcaster_id={self.broadcaster_id}&moderator_id={self.broadcaster_id}"
                data = {
                    "data": {
                        "user_id": user_id,
                        "duration": duration,
                        "reason": "No reason provided"  # You can customize the reason
                    }
                }
                response = requests.post(url, headers=self.get_headers(), json=data)
                if response.status_code == 200:
                    await ctx.send(f"{user} has been timed out for {duration} seconds.")
                else:
                    await ctx.send(f"Failed to timeout {user}. API returned {response.status_code}: {response.json().get('message')}")
            else:
                await ctx.send(f"User {user} not found.")
        else:
            await ctx.send("You do not have permission to use this command.")

    @commands.command(name='unban')
    async def unban_user(self, ctx, user: str):
        """Unban a user from the channel. Usage: !unban <username>"""
        if ctx.author.is_mod:
            user_id = self.get_user_id(user)
            if user_id:
                url = f"https://api.twitch.tv/helix/moderation/bans?broadcaster_id={self.broadcaster_id}&moderator_id={self.broadcaster_id}&user_id={user_id}"
                response = requests.delete(url, headers=self.get_headers())
                if response.status_code == 204:
                    await ctx.send(f"{user} has been unbanned.")
                else:
                    await ctx.send(f"Failed to unban {user}. API returned {response.status_code}: {response.json().get('message')}")
            else:
                await ctx.send(f"User {user} not found.")
        else:
            await ctx.send("You do not have permission to use this command.")

def prepare(bot):
    bot.add_cog(Moderation(bot))
