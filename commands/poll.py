import os
import requests
from twitchio.ext import commands

class Poll(commands.Cog):

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

    @commands.command(name='poll')
    async def create_poll(self, ctx, title: str, *choices: str):
        """Create a poll with a title and up to 5 choices. Usage: !poll "Poll Title" "Choice 1" "Choice 2" ..."""
        if ctx.author.is_mod:
            if len(choices) < 2 or len(choices) > 5:
                await ctx.send("You must provide between 2 to 5 choices for the poll.")
                return
            
            url = f"https://api.twitch.tv/helix/polls"
            data = {
                "broadcaster_id": self.broadcaster_id,
                "title": title,
                "choices": [{"title": choice} for choice in choices],
                "duration": 300  # Poll duration in seconds (5 minutes)
            }
            response = requests.post(url, headers=self.get_headers(), json=data)
            if response.status_code == 200:
                poll_data = response.json()['data'][0]
                await ctx.send(f"Poll created! Title: {poll_data['title']} | Choices: {', '.join(choice['title'] for choice in poll_data['choices'])}")
            else:
                await ctx.send(f"Failed to create poll. API returned {response.status_code}: {response.json().get('message')}")
        else:
            await ctx.send("You do not have permission to use this command.")

def prepare(bot):
    bot.add_cog(Poll(bot))
