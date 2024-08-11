from twitchio.ext import commands
import requests
import os

class Followage(commands.Cog):

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

    @commands.command(name='followage')
    async def followage(self, ctx, username: str = None):
        if not username:
            username = ctx.author.name

        user_id = self.get_user_id(username)
        if not user_id:
            await ctx.send(f"User {username} not found.")
            return

        url = f"https://api.twitch.tv/helix/users/follows?to_id={self.broadcaster_id}&from_id={user_id}"
        response = requests.get(url, headers=self.get_headers())
        data = response.json().get('data', [])

        if not data:
            await ctx.send(f"{username} is not following the channel.")
            return

        follow_data = data[0]
        follow_date = follow_data['followed_at']
        await ctx.send(f"{username} has been following since {follow_date}.")

def prepare(bot):
    bot.add_cog(Followage(bot))
