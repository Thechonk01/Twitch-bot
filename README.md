# Twitch-bot
 Twitch bot in python
# Twitch Bot

This is a Twitch bot built using Python and the TwitchIO library. The bot provides various moderation, utility, and interactive commands for streamers and their communities.

## Features

- **Moderation Commands**
  - !ban `<username>`: Ban a user from the channel.
  - !timeout `<username> <duration_in_seconds>`: Timeout a user from the channel.
  - !unban `<username>`: Unban a user from the channel.

- **Utility Commands**
  - !poll `"Poll Title" "Choice 1" "Choice 2" ...`: Create a poll with a title and up to 5 choices.
  - !raid `<target_channel>`: Start a raid to another channel.
  - !clip: Create a clip from the current stream.

- **Community Commands**
  - !discord: Get the link to the Discord server.
  - !socials: Get links to social media channels.
  - !lurk: Notify that you are lurking.
  - !unlurk: Notify that you are back from lurking.

- **Stream Management Commands**
  - !game `<game>` (mod only): Update the stream game or use !game to get the current game.
  - !title `<title>` (mod only): Update the stream title or use !title to get the current title.

- **Help Command**
  - !commands `<command_name>`: Get the usage information for a specific command.

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/twitch-bot.git
cd twitch-bot
```

2. **Create and activate a virtual environment (optional but recommended):**
   - `python -m venv venv`
   - On Windows use: `venv\Scripts\activate`
   - On macOS/Linux use: `source venv/bin/activate`

3. **Install the required dependencies:**
```py
pip install -r requirements.txt
```
5. **Create a `.env` file:**
   In the root directory of the project, create a `.env` file with the following content:
```.env
TWITCH_OAUTH_TOKEN=oauth:your_oauth_token_here
TWITCH_CLIENT_ID=your_client_id_here
TWITCH_CLIENT_SECRET=your_client_secret_here
TWITCH_USERNAME=your_bot_username_here
TWITCH_CHANNEL=your_channel_name_here
```
   Replace `your_oauth_token_here`, `your_client_id_here`, `your_client_secret_here`, `your_bot_username_here`, and `your_channel_name_here` with your actual Twitch credentials.

5. **Run the bot:**
```py
python bot.py
```
## Usage

- Once the bot is running, it will join the specified Twitch channel and start listening for commands.
- Use the commands listed in the **Features** section directly in the Twitch chat.
- To get help for a specific command, use `!commands <command_name>`.

## Adding New Commands

To add new commands, you can create new Python files in the `commands` directory or add them to an existing file. Ensure that each command is registered correctly using the `@commands.command()` decorator.

Example of a new command:

```python
from twitchio.ext import commands

class MyCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        """Say hello to the bot. Usage: !hello"""
        await ctx.send(f'Hello, {ctx.author.name}!')

def prepare(bot):
    bot.add_cog(MyCommands(bot))
```

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- TwitchIO: The Python library used to build this bot.
- Twitch Developers: For providing the APIs and documentation.

### Happy Streaming!
