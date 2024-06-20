import interactions
import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = interactions.Client(token=BOT_TOKEN)

CACHE_DIR = "pokemon_cache"
CACHE_EXPIRY_DAYS = 14

# Ensure the cache directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_cache_filepath(name, cache_type):
    return os.path.join(CACHE_DIR, f"{cache_type}_{name.lower()}.json")

def load_cache(name, cache_type):
    filepath = get_cache_filepath(name, cache_type)
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            cache_data = json.load(file)
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cache_time < timedelta(days=CACHE_EXPIRY_DAYS):
                return cache_data['data']
    return None

def save_cache(name, cache_type, data):
    filepath = get_cache_filepath(name, cache_type)
    with open(filepath, 'w') as file:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': data
        }, file)

@interactions.listen()
async def on_ready():
    bot_user = await bot.fetch_user(bot.user.id)
    print(f'Logged in as {bot_user.username}')

@interactions.slash_command(
    name="pokemon",
    description="Get information about a Pokémon",
    options=[
        interactions.SlashCommandOption(
            name="pokemon_name",
            description="Name of the Pokémon",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def slash_get_pokemon(ctx: interactions.SlashContext, pokemon_name: str):
    data = load_cache(pokemon_name, 'pokemon')
    if not data:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
        if response.status_code == 200:
            data = response.json()
            save_cache(pokemon_name, 'pokemon', data)
        else:
            await ctx.send(f'Could not find Pokémon named "{pokemon_name}".')
            return

    name = data['name'].capitalize()
    height = data['height']
    weight = data['weight']
    types = ', '.join([t['type']['name'] for t in data['types']])
    abilities = ', '.join([a['ability']['name'] for a in data['abilities']])
    sprite_url = data['sprites']['front_default']
    
    await ctx.send(
        f'**{name}**\nHeight: {height}\nWeight: {weight}\nTypes: {types}\nAbilities: {abilities}\n[Image Link]({sprite_url})'
    )

@interactions.slash_command(
    name="item",
    description="Get information about an item",
    options=[
        interactions.SlashCommandOption(
            name="item_name",
            description="Name of the item",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def slash_get_item(ctx: interactions.SlashContext, item_name: str):
    data = load_cache(item_name, 'item')
    if not data:
        response = requests.get(f'https://pokeapi.co/api/v2/item/{item_name.lower()}')
        if response.status_code == 200:
            data = response.json()
            save_cache(item_name, 'item', data)
        else:
            await ctx.send(f'Could not find item named "{item_name}".')
            return

    name = data['name'].capitalize()
    cost = data['cost']
    effect = data['effect_entries'][0]['effect']
    sprite_url = data['sprites']['default']
    
    await ctx.send(
        f'**{name}**\nCost: {cost}\nEffect: {effect}\n[Image Link]({sprite_url})'
    )

bot.start()
