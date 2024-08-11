from twitchio.ext import commands
import requests
import os

class Subcount(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.token = os.getenv('TWITCH_OAUTH_TOKEN').split(':')[1]
        self.broadcaster_id = self.get_user_id(os.getenv('TWITCH_CHANNEL'))

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Client-Id': self.client_id
        }

    def get_user_id(self, username):
        url = f"https://api.twitch.tv/helix/users?login={username}"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200 and response.json()['data']:
            return response.json()['data'][0]['id']
        return None

    @commands.command(name='subcount')
    async def subcount(self, ctx):
        url = f"https://api.twitch.tv/helix/subscriptions?broadcaster_id={self.broadcaster_id}"
        response = requests.get(url, headers=self.get_headers())
        data = response.json().get('data', [])

        subcount = len(data)
        await ctx.send(f"The channel currently has {subcount} subscribers.")

def prepare(bot):
    bot.add_cog(Subcount(bot))
