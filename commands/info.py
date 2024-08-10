from twitchio.ext import commands
import requests
import os

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.token = os.getenv('TWITCH_OAUTH_TOKEN').split(':')[1]
        self.channel_id = self.get_channel_id()

    def get_headers(self):
        return {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def get_channel_id(self):
        url = f'https://api.twitch.tv/helix/users?login={os.getenv("TWITCH_CHANNEL")}'
        response = requests.get(url, headers=self.get_headers())
        return response.json()['data'][0]['id'] if response.status_code == 200 else None

    def get_stream_info(self):
        url = f'https://api.twitch.tv/helix/channels?broadcaster_id={self.channel_id}'
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            return response.json()['data'][0]
        return None

    @commands.command(name='title')
    async def title(self, ctx, *, title: str = None):
        """Update the stream title. Usage: !title <title> (mod only) | !title (to get the current title)"""
        if title:  # If a title is provided, update the stream title
            if ctx.author.is_mod:
                url = f'https://api.twitch.tv/helix/channels?broadcaster_id={self.channel_id}'
                payload = {
                    'title': title
                }
                response = requests.patch(url, headers=self.get_headers(), json=payload)
                if response.status_code == 204:
                    await ctx.send(f'Stream title updated to: {title}')
                else:
                    print(response.json())
                    await ctx.send('Failed to update title.')
            else:
                await ctx.send("You do not have permission to use this command.")
        else:  # If no title is provided, return the current title
            stream_info = self.get_stream_info()
            if stream_info:
                current_title = stream_info['title']
                await ctx.send(f'Current stream title: {current_title}')
            else:
                await ctx.send("Could not retrieve the current title.")

    @commands.command(name='game') 
    async def game(self, ctx, *, game: str = None):
        """Update the stream game. Usage: !game <game> (mod only) | !game (to get the current game)"""
        if game:  # If a game is provided, update the stream game
            if ctx.author.is_mod:
                # Get the game ID
                game_url = f'https://api.twitch.tv/helix/games?name={game}'
                game_response = requests.get(game_url, headers=self.get_headers())
                if game_response.status_code == 200 and game_response.json()['data']:
                    game_id = game_response.json()['data'][0]['id']

                    # Update the game
                    url = f'https://api.twitch.tv/helix/channels?broadcaster_id={self.channel_id}'
                    payload = {
                        'game_id': game_id
                    }
                    response = requests.patch(url, headers=self.get_headers(), json=payload)
                    if response.status_code == 204:
                        await ctx.send(f'Stream game updated to: {game}')
                    else:
                        await ctx.send('Failed to update game.')
                else:
                    await ctx.send(f'Game "{game}" not found.')
            else:
                await ctx.send("You do not have permission to use this command.")
        else:  # If no game is provided, return the current game
            stream_info = self.get_stream_info()
            if stream_info:
                game_id = stream_info['game_id']
                game_url = f'https://api.twitch.tv/helix/games?id={game_id}'
                game_response = requests.get(game_url, headers=self.get_headers())
                if game_response.status_code == 200 and game_response.json()['data']:
                    current_game = game_response.json()['data'][0]['name']
                    await ctx.send(f'Current stream game: {current_game}')
                else:
                    await ctx.send("Could not retrieve the current game.")
            else:
                await ctx.send("Could not retrieve the current game.")

def prepare(bot):
    bot.add_cog(Info(bot))
