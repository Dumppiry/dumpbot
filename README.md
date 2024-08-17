# dumpbot

Discord bot because discord is best

## Development

### Presequites

- Python 3.12 or higher
- make

Check python version.

Instal required software.

```bash
sudo apt install make
```

Clone the repository

```bash
git clone git@github.com:Dumppiry/dumpbot.git
```

### Set up python

Minimum Python version required is 3.12. You can check your python version with following.

```bash
python3 --version
```

Create and activate venv.

```bash
python3 -m venv venv
. ./venv/bin/activate
```

Install requirements.

```bash
pip3 install -r requirements.txt
```

Create new branch for your development.

```bash
git checkout -b <branch-name>
```

### Running the program

First you need to create `.env.dev` file.

```bash
cp .env.example .env.dev
```

Fill in the variables.
| Variable | description |
| :---: | --- |
| DISCORD_TOKEN | This is the api token for discord bot. Use the DumpBotDev token for this. Ask for this token from webmaster. |
| GUILD_ID | Guild id of the server used for development.

Run the program in development mode with Make.

```bash
make dev
```

## How to add commands

Mostly the development is probably adding new commands or functionality to old ones. All the commands are loaded from the `src/dumpbot/commands` package. This package publishes variables called `commands` and `dev_commands` in the `__init__.py`. Commands are added to the bot from these variables.

### Creating a command

To create a command, first decide if it is a normal command or dev command.

- Dev commands are commands that are used only during development and they are found under `src/dumpbot/commands/_dev_commands` and are imported to `dev_commands` variable.

- Normal commands are used in the production bot and are under `src/dumpbot/commands/_commands` and are imported to the `commands` variable.

Now create a new file under selected directory and name it as `<command name>.py`. This python file should declare at least one variable which is `app_commands.Command` and a callback function for it.

```python
# src/dumpbot/commands/_dev_commands/ping.py
import discord
from discord import app_commands

async def callback(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

ping = app_commands.Command(
    name="ping",
    description="A simple ping command",
    callback=callback,
)
```

Then you should also import this in the file `src/dumpbot/commands/__init__.py` to the correct variable.

```python
from ._dev_commands.some_command import some_command
from ._dev_commands.ping import ping # Import the command

dev_commands = [some_command, ping] # Add it to the variable
```

Rerun the bot and test the command!

## Pushing to prod

When your modifications are ready to be published, create a pull request against `main` branch from your branch. It will be reviewed and (hopefully soon automated tests will be run). When all is green, the pr will be merged to main and will be available in the production.

> You can also ping @Dev in our discords development channel and ask for it to be reviewed.
