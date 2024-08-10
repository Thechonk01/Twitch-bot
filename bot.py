import os
from twitchio.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Bot(commands.Bot):

    def __init__(self):
        token = os.getenv('TWITCH_OAUTH_TOKEN')
        prefix = '!'
        initial_channels = [os.getenv('TWITCH_CHANNEL')]

        # Initialize the bot with the token, prefix, and initial channels
        super().__init__(token=token, prefix=prefix, initial_channels=initial_channels)

        # Load all command modules (cogs)
        self.load_module('commands.moderation')  # Assuming all moderation commands are here
        self.load_module('commands.poll')        # Assuming the poll command is here
        self.load_module('commands.raid')        # Assuming the raid command is here
        self.load_module('commands.clip')        # Assuming the clip command is here
        self.load_module('commands.socials')     # Assuming socials command is here
        self.load_module('commands.lurk')        # Assuming lurk and unlurk commands are here
        self.load_module('commands.info')        # Assuming info command is here
        self.load_module('commands.commands')# Assuming the commands command is here

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

# Create and run the bot
bot = Bot()
bot.run()
