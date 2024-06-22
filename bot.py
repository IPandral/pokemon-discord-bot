import os
from dotenv import load_dotenv
import interactions
import requests
import json
from datetime import datetime, timedelta
import asyncio
import hashlib
import random
from recommended_builds import get_recommended_build

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise RuntimeError("No token provided - please set the BOT_TOKEN environment variable.")

# Initialize bot
bot = interactions.Client(token=BOT_TOKEN)

def url_to_filename(url):
    return hashlib.md5(url.encode()).hexdigest()

def load_cache(key, cache_type):
    filename = url_to_filename(key)
    try:
        with open(f'cache/{cache_type}/{filename}.json', 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return None

def save_cache(key, cache_type, data):
    filename = url_to_filename(key)
    os.makedirs(f'cache/{cache_type}', exist_ok=True)
    with open(f'cache/{cache_type}/{filename}.json', 'w') as f:
        json.dump(data, f)

async def get_pokemon_details(name: str):
    try:
        data = load_cache(name, 'pokemon')
        if not data:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name.lower()}/')
            if response.status_code == 200:
                data = response.json()
                save_cache(name, 'pokemon', data)
            else:
                return None

        species_data = load_cache(name, 'pokemon_species')
        if not species_data:
            species_response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{name.lower()}/')
            if species_response.status_code == 200:
                species_data = species_response.json()
                save_cache(name, 'pokemon_species', species_data)
            else:
                return None

        evolution_chain_url = species_data['evolution_chain']['url']
        evolution_chain_key = url_to_filename(evolution_chain_url)
        evolution_data = load_cache(evolution_chain_key, 'evolution_chain')
        if not evolution_data:
            evolution_response = requests.get(evolution_chain_url)
            if evolution_response.status_code == 200:
                evolution_data = evolution_response.json()
                save_cache(evolution_chain_key, 'evolution_chain', evolution_data)
            else:
                return None

        # Get detailed stats
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        hp = stats['hp']
        attack = stats['attack']
        defense = stats['defense']
        special_attack = stats['special-attack']
        special_defense = stats['special-defense']
        speed = stats['speed']

        # Get movesets
        moves = data['moves']
        level_up_moves = [move['move']['name'] for move in moves if any(version['move_learn_method']['name'] == 'level-up' for version in move['version_group_details'])]
        egg_moves = [move['move']['name'] for move in moves if any(version['move_learn_method']['name'] == 'egg' for version in move['version_group_details'])]

        # Get held items
        held_items = [item['item']['name'] for item in data['held_items']]

        # Get abilities
        abilities = [ability['ability']['name'] for ability in data['abilities']]
        
        # Get breeding information
        egg_groups = [egg_group['name'] for egg_group in species_data['egg_groups']]
        gender_rate = species_data['gender_rate']
        capture_rate = species_data['capture_rate']

        # Get type effectiveness
        types = [t['type']['name'] for t in data['types']]
        type_data = []
        for t in types:
            type_response = requests.get(f'https://pokeapi.co/api/v2/type/{t}')
            if type_response.status_code == 200:
                type_data.append(type_response.json())

        strong_against = []
        weak_against = []
        for t in type_data:
            strong_against += [t['name'] for t in t['damage_relations']['double_damage_to']]
            weak_against += [t['name'] for t in t['damage_relations']['double_damage_from']]
        
        # Get encounters
        encounter_url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}/encounters'
        encounter_response = requests.get(encounter_url)
        if encounter_response.status_code == 200:
            encounters = encounter_response.json()
            encounter_locations = [encounter['location_area']['name'] for encounter in encounters]
        else:
            encounter_locations = []

        # Recommended build
        recommended_build = get_recommended_build(name.lower())

        # Constructing the response
        sprite_url = data['sprites']['front_default']
        response_text = (
            f'**{name.capitalize()} Details**\n'
            f'**Height**: {data["height"] / 10} m\n'
            f'**Weight**: {data["weight"] / 10} kg\n'
            f'**Types**: {", ".join(types)}\n'
            f'**Abilities**: {", ".join(abilities)}\n'
            f'**Evolution Chain**: {format_evolution_chain(evolution_data["chain"])}\n'
            f'**Strong Against**: {", ".join(strong_against)}\n'
            f'**Weak Against**: {", ".join(weak_against)}\n'
            f'**Encounter Locations**: {", ".join(encounter_locations)}\n'
            f'**Held Items**: {", ".join(held_items)}\n'
            f'**Egg Groups**: {", ".join(egg_groups)}\n'
            f'**Gender Ratio (Female:Male)**: {gender_rate * 12.5}% : {(8 - gender_rate) * 12.5}%\n'
            f'**Capture Rate**: {capture_rate}\n\n'
            f'**Stats**:\n'
            f'HP: {hp}\n'
            f'Attack: {attack}\n'
            f'Defense: {defense}\n'
            f'Special Attack: {special_attack}\n'
            f'Special Defense: {special_defense}\n'
            f'Speed: {speed}\n\n'
            f'**Level-Up Moves**: {", ".join(level_up_moves[:20])}\n\n'  # Limit to 20 moves
            f'**Egg Moves**: {", ".join(egg_moves[:20])}\n\n'  # Limit to 20 moves
            f'**Recommended Build**:\n{recommended_build}\n'
            f'[Image]({sprite_url})\n'
        )

        return response_text

    except Exception as e:
        print(f"Error fetching Pokémon details: {e}")
        return f"An error occurred while fetching the Pokémon details: {e}"

def format_evolution_chain(chain):
    evo_chain = []
    current = chain
    while current:
        evo_chain.append(current['species']['name'])
        current = current['evolves_to'][0] if current['evolves_to'] else None
    return " ➔ ".join(evo_chain)

@interactions.slash_command(
    name="pokemon",
    description="Get information about a Pokémon",
    options=[
        interactions.SlashCommandOption(
            name="name",
            description="Name of the Pokémon",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def slash_get_pokemon(ctx: interactions.SlashContext, name: str):
    await ctx.defer()  # Defer the response to avoid timeout
    response_text = await get_pokemon_details(name)
    await ctx.send(response_text[:2000])  # Ensure message length is within Discord's limit

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
    await ctx.defer()  # Defer the response to avoid timeout

    try:
        data = load_cache(item_name, 'item')
        if not data:
            response = requests.get(f'https://pokeapi.co/api/v2/item/{item_name.lower()}/')
            if response.status_code == 200:
                data = response.json()
                save_cache(item_name, 'item', data)
            else:
                await ctx.send(f'Could not find item named "{item_name}".')
                return

        cost = data['cost']
        effect_entries = data['effect_entries']
        short_effect = effect_entries[0]['short_effect'] if effect_entries else 'No effect description available'
        sprite_url = data['sprites']['default']

        response_text = (
            f'**{item_name.capitalize()}**\n'
            f'**Cost**: {cost} gold\n'
            f'**Effect**: {short_effect}\n'
            f'**Image Link**: [Image]({sprite_url})'
        )

        await ctx.send(response_text)

    except Exception as e:
        print(f"Error fetching item: {e}")
        await ctx.send(f"An error occurred while fetching the item: {e}")

# Reminder Command
reminders = {}

@interactions.slash_command(
    name="remind",
    description="Set a reminder",
    options=[
        interactions.SlashCommandOption(
            name="time",
            description="Time in minutes",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
        interactions.SlashCommandOption(
            name="message",
            description="Reminder message",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def set_reminder(ctx: interactions.SlashContext, time: int, message: str):
    remind_time = datetime.now() + timedelta(minutes=time)
    reminders[ctx.author.id] = (remind_time, message)
    await ctx.send(f'Reminder set for {time} minutes.')

async def check_reminders():
    while True:
        now = datetime.now()
        for user_id, (remind_time, message) in list(reminders.items()):
            if now >= remind_time:
                user = await bot.fetch_user(user_id)
                await user.send(f'Reminder: {message}')
                del reminders[user_id]
        await asyncio.sleep(60)

@interactions.slash_command(
    name="random_pokemon",
    description="Get information about a random Pokémon",
)
async def slash_get_random_pokemon(ctx: interactions.SlashContext):
    await ctx.defer()  # Defer the response to avoid timeout

    try:
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1000')
        if response.status_code == 200:
            data = response.json()
            random_pokemon = random.choice(data['results'])
            pokemon_name = random_pokemon['name']
            response_text = await get_pokemon_details(pokemon_name)
            await ctx.send(response_text[:2000])  # Ensure message length is within Discord's limit
        else:
            await ctx.send('Could not retrieve Pokémon list.')

    except Exception as e:
        print(f"Error fetching random Pokémon: {e}")
        await ctx.send(f"An error occurred while fetching a random Pokémon: {e}")

@interactions.slash_command(
    name="pokemon_of_the_day",
    description="Get information about the Pokémon of the day",
)
async def slash_get_pokemon_of_the_day(ctx: interactions.SlashContext):
    await ctx.defer()  # Defer the response to avoid timeout

    try:
        today = datetime.now().strftime("%Y-%m-%d")
        data = load_cache(today, 'pokemon_of_the_day')
        if not data:
            response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1000')
            if response.status_code == 200:
                all_pokemon = response.json()['results']
                pokemon_name = random.choice(all_pokemon)['name']
                response_text = await get_pokemon_details(pokemon_name)
                save_cache(today, 'pokemon_of_the_day', {'pokemon_name': pokemon_name})
                await ctx.send(response_text[:2000])  # Ensure message length is within Discord's limit
            else:
                await ctx.send('Could not retrieve Pokémon list.')

        else:
            pokemon_name = data['pokemon_name']
            response_text = await get_pokemon_details(pokemon_name)
            await ctx.send(response_text[:2000])  # Ensure message length is within Discord's limit

    except Exception as e:
        print(f"Error fetching Pokémon of the day: {e}")
        await ctx.send(f"An error occurred while fetching the Pokémon of the day: {e}")

@interactions.slash_command(
    name="help",
    description="Get a list of all commands",
)
async def slash_help(ctx: interactions.SlashContext):
    help_text = (
        "**PokeBot Commands**\n\n"
        "/pokemon `name`: Get detailed information about a specific Pokémon.\n"
        "/item `item_name`: Get information about a specific item.\n"
        "/remind `time` `message`: Set a reminder that will notify you after a specified time.\n"
        "/random_pokemon: Get information about a random Pokémon.\n"
        "/pokemon_of_the_day: Get information about the Pokémon of the day.\n"
    )
    await ctx.send(help_text)

# Start the check_reminders task
@bot.event
async def on_ready():
    print(f'Logged in as {bot.me.name}')
    # Start the reminder checker
    asyncio.create_task(check_reminders())

# Run the bot
bot.start()
