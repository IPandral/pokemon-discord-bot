import interactions
import requests
import os
import json
from datetime import datetime, timedelta
import asyncio
import hashlib
from dotenv import load_dotenv

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
    await ctx.defer()  # Defer the response to avoid timeout

    data = load_cache(pokemon_name, 'pokemon')
    if not data:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/')
        if response.status_code == 200:
            data = response.json()
            save_cache(pokemon_name, 'pokemon', data)
        else:
            await ctx.send(f'Could not find Pokémon named "{pokemon_name}".')
            return

    # Basic Info
    height = data['height'] / 10  # decimeters to meters
    weight = data['weight'] / 10  # hectograms to kilograms
    types = [t['type']['name'] for t in data['types']]
    abilities = [a['ability']['name'] for a in data['abilities']]
    sprite_url = data['sprites']['front_default']

    # Evolution Chain
    species_data = load_cache(data['species']['url'], 'pokemon_species')
    if not species_data:
        species_response = requests.get(data['species']['url'])
        if species_response.status_code == 200:
            species_data = species_response.json()
            save_cache(data['species']['url'], 'pokemon_species', species_data)
        else:
            await ctx.send(f'Could not retrieve species data for "{pokemon_name}".')
            return
    
    evolution_chain_url = species_data['evolution_chain']['url']
    evolution_data = load_cache(evolution_chain_url, 'evolution_chain')
    if not evolution_data:
        response = requests.get(evolution_chain_url)
        if response.status_code == 200:
            evolution_data = response.json()
            save_cache(evolution_chain_url, 'evolution_chain', evolution_data)
        else:
            await ctx.send(f'Could not retrieve evolution chain for "{pokemon_name}".')
            return

    evolution_chain = []
    current = evolution_data['chain']
    while current:
        species_name = current['species']['name'].capitalize()
        evolution_chain.append(species_name)
        if current['evolves_to']:
            current = current['evolves_to'][0]
        else:
            break

    chain_text = ' ➔ '.join(evolution_chain)

    # Type Effectiveness
    effectiveness = load_cache('type_effectiveness', 'type_effectiveness')
    if not effectiveness:
        response = requests.get('https://pokeapi.co/api/v2/type/')
        if response.status_code == 200:
            effectiveness = response.json()
            save_cache('type_effectiveness', 'type_effectiveness', effectiveness)
        else:
            await ctx.send(f'Could not retrieve type effectiveness data.')
            return

    strong_against = []
    weak_against = []
    for t in types:
        type_data = next((item for item in effectiveness['results'] if item['name'] == t), None)
        if type_data:
            type_detail = load_cache(type_data['url'], 'type')
            if not type_detail:
                response = requests.get(type_data['url'])
                if response.status_code == 200:
                    type_detail = response.json()
                    save_cache(type_data['url'], 'type', type_detail)
                else:
                    await ctx.send(f'Could not retrieve type data for "{t}".')
                    return
            
            strong_against.extend([x['name'] for x in type_detail['damage_relations']['double_damage_to']])
            weak_against.extend([x['name'] for x in type_detail['damage_relations']['double_damage_from']])

    strong_against = set(strong_against)
    weak_against = set(weak_against)

    # Encounters
    encounter_data = load_cache(pokemon_name, 'encounters')
    if not encounter_data:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/encounters')
        if response.status_code == 200:
            encounter_data = response.json()
            save_cache(pokemon_name, 'encounters', encounter_data)
        else:
            await ctx.send(f'Could not retrieve encounter data for "{pokemon_name}".')
            return

    encounter_locations = [e['location_area']['name'].replace('-', ' ').capitalize() for e in encounter_data]

    # Build and send the response
    response_text = (
        f'**{pokemon_name.capitalize()}**\n'
        f'**Height**: {height} m\n'
        f'**Weight**: {weight} kg\n'
        f'**Types**: {", ".join(types)}\n'
        f'**Abilities**: {", ".join(abilities)}\n'
        f'**Evolution Chain**: {chain_text}\n'
        f'**Strong Against**: {", ".join(strong_against)}\n'
        f'**Weak Against**: {", ".join(weak_against)}\n'
        f'**Encounter Locations**: {", ".join(encounter_locations)}\n'
        f'**Image Link**: [Image]({sprite_url})'
    )

    await ctx.send(response_text)

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

# Start the check_reminders task
@bot.event
async def on_ready():
    print(f'Logged in as {bot.me.name}')
    # Start the reminder checker
    asyncio.create_task(check_reminders())

# Run the bot
bot.start()
