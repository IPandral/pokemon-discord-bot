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
/pokemon Charizard

```
<img width="857" alt="Charizard-Example" src="https://github.com/IPandral/pokemon-discord-bot/assets/53560986/167661eb-0e24-4e59-a047-209db8ea4d88">

### `/item item_name`

Get information about a specific item.

Example:
```
/item Potion
```
<img width="380" alt="item-example" src="https://github.com/IPandral/pokemon-discord-bot/assets/53560986/08419ff9-45d5-4351-b9df-444aba116e5b">


### `/remind time message`

Set a reminder that the bot will notify you about after the specified time.

Example:
```
/remind 10 eggs-hatched
```
<img width="269" alt="reminder-example" src="https://github.com/IPandral/pokemon-discord-bot/assets/53560986/4163ae25-f074-447c-902b-668c18d17453">


### `/random_pokemon`

Get information about a random Pokémon.
<img width="870" alt="random-example" src="https://github.com/IPandral/pokemon-discord-bot/assets/53560986/e4fc08cb-cc17-4349-abde-42fbc48a8ff0">


### `/pokemon_of_the_day`

Get information about the Pokémon of the day.
<img width="907" alt="pokemon-of-the-day" src="https://github.com/IPandral/pokemon-discord-bot/assets/53560986/ff1098b4-b92d-481b-a865-daae64644d43">


### `/help`

Get a list of available commands and their descriptions.
<img width="634" alt="help-example" src="https://github.com/IPandral/pokemon-discord-bot/assets/53560986/d2b21681-997f-4b56-bbd6-ea81e96f24f6">


## Installation

1. Clone the repository:
```
git clone https://github.com/IPandral/pokemon-discord-bot.git
cd pokemon-discord-bot
```

2. Build and run the Docker container:
```
docker build -t pokebot .
docker run -d --name='pokebot' --net='bridge' -e TZ="Australia/Perth" -e HOST_OS="OS" -e HOST_HOSTNAME="Name" -e HOST_CONTAINERNAME="pokebot" -l net.unraid.docker.managed=dockerman -e BOT_TOKEN=your_discord_bot_token pokebot:latest
```

## Usage

Invite the bot to your Discord server using the OAuth2 URL with the appropriate permissions. Once invited, use the commands listed above to interact with the bot.

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request. We welcome all improvements, including new features, bug fixes, and documentation updates.

## License

This project is licensed under the MIT License.
