recommended_builds = {
    'bulbasaur': {
        'moves': ['Sludge Bomb', 'Giga Drain', 'Leech Seed', 'Protect'],
        'held_item': 'Leftovers',
        'ev_spread': {'HP': 252, 'Defense': 252, 'Special Defense': 4},
        'nature': 'Bold'
    },
    'charmander': {
        'moves': ['Flamethrower', 'Dragon Pulse', 'Ancient Power', 'Fire Spin'],
        'held_item': 'Charcoal',
        'ev_spread': {'Special Attack': 252, 'Speed': 252, 'HP': 4},
        'nature': 'Timid'
    },
    'squirtle': {
        'moves': ['Scald', 'Ice Beam', 'Rapid Spin', 'Toxic'],
        'held_item': 'Eviolite',
        'ev_spread': {'HP': 252, 'Defense': 252, 'Special Defense': 4},
        'nature': 'Bold'
    },
    'pikachu': {
        'moves': ['Thunderbolt', 'Volt Tackle', 'Iron Tail', 'Quick Attack'],
        'held_item': 'Light Ball',
        'ev_spread': {'Attack': 252, 'Speed': 252, 'HP': 4},
        'nature': 'Jolly'
    },
    'chikorita': {
        'moves': ['Energy Ball', 'Reflect', 'Light Screen', 'Leech Seed'],
        'held_item': 'Light Clay',
        'ev_spread': {'HP': 252, 'Defense': 252, 'Special Defense': 4},
        'nature': 'Calm'
    },
    'cyndaquil': {
        'moves': ['Flamethrower', 'Eruption', 'Solar Beam', 'Hidden Power Grass'],
        'held_item': 'Choice Scarf',
        'ev_spread': {'Special Attack': 252, 'Speed': 252, 'HP': 4},
        'nature': 'Modest'
    },
    'totodile': {
        'moves': ['Waterfall', 'Ice Fang', 'Crunch', 'Dragon Dance'],
        'held_item': 'Life Orb',
        'ev_spread': {'Attack': 252, 'Speed': 252, 'HP': 4},
        'nature': 'Adamant'
    },
    # Add more starter Pokémon builds here...
    'charizard': {
        'moves': ['Flamethrower', 'Dragon Claw', 'Roost', 'Solar Beam'],
        'held_item': 'Charizardite Y',
        'ev_spread': {'Special Attack': 252, 'Speed': 252, 'HP': 4},
        'nature': 'Timid'
    },
    'snorlax': {
        'moves': ['Body Slam', 'Earthquake', 'Rest', 'Sleep Talk'],
        'held_item': 'Leftovers',
        'ev_spread': {'HP': 252, 'Defense': 252, 'Special Defense': 4},
        'nature': 'Careful'
    },
}

def get_recommended_build(pokemon_name):
    build = recommended_builds.get(pokemon_name.lower())
    if build:
        return (
            f"**Moves**: {', '.join(build['moves'])}\n"
            f"**Held Item**: {build['held_item']}\n"
            f"**EV Spread**: {', '.join([f'{stat}: {value}' for stat, value in build['ev_spread'].items()])}\n"
            f"**Nature**: {build['nature']}"
        )
    else:
        return "Recommended build will be available soon."