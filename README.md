
# Pokémon Discord Bot

This is a Discord bot that provides detailed information about Pokémon. It can fetch Pokémon details, including stats, evolution chains, type effectiveness, encounter locations, and recommended builds. It also supports setting reminders and fetching random Pokémon or Pokémon of the day.

## Features

- Get detailed Pokémon information:
  - Basic stats (HP, Attack, Defense, etc.)
  - Evolution chain
  - Type effectiveness
  - Encounter locations
  - Held items
  - Abilities
  - Breeding information
  - Recommended competitive builds
- Set reminders
- Fetch a random Pokémon
- Fetch the Pokémon of the day

## Commands

### `/pokemon name`

Get detailed information about a specific Pokémon.

Example:
```
/pokemon Pikachu
```

### `/item item_name`

Get information about a specific item.

Example:
```
/item Potion
```

### `/remind time message`

Set a reminder that the bot will notify you about after the specified time.

Example:
```
/remind 10 eggs-hatched
```

### `/random_pokemon`

Get information about a random Pokémon.

### `/pokemon_of_the_day`

Get information about the Pokémon of the day.

### `/help`

Get a list of available commands and their descriptions.

## Installation

1. Clone the repository:
```
git clone https://github.com/IPandral/pokemon-discord-bot.git
cd pokemon-discord-bot
```

2. Build and run the Docker container:
```
docker build -t pokemon-discord-bot .
docker run -d --name='pokebot' --net='bridge' -e TZ="Australia/Perth" -e HOST_OS="OS" -e HOST_HOSTNAME="Name" -e HOST_CONTAINERNAME="pokebot" -l net.unraid.docker.managed=dockerman -e BOT_TOKEN=your_discord_bot_token pokemon-discord-bot:latest
```
Replace "your_discord_bot_token" with your actual discord bot token from [Discord Developer Portal](https://discord.com/developers/applications)

## deploy from my docker Hub Repo
```
docker run -d --name='pokebot' --net='bridge' -e TZ="Australia/Perth" -e HOST_OS="OS" -e HOST_HOSTNAME="Name" -e HOST_CONTAINERNAME="pokebot" -l net.unraid.docker.managed=dockerman -e BOT_TOKEN=your_discord_bot_token ipandral/pokemon-discord-bot:latest
```
Replace "your_discord_bot_token" with your actual discord bot token from [Discord Developer Portal](https://discord.com/developers/applications)

[Docker Hub Repo](https://hub.docker.com/repository/docker/ipandral/pokemon-discord-bot/general)

## Usage

Invite the bot to your Discord server using the OAuth2 URL with the appropriate permissions. Once invited, use the commands listed above to interact with the bot.

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request. We welcome all improvements, including new features, bug fixes, and documentation updates.

## License

This project is licensed under the MIT License.
