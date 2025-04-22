from typing import Dict
from .consts import BIOMES

def process_biome(biome_data: Dict):
    biome_id = biome_data["biome"]
    ac_parameters = BIOMES[biome_id]
    print(f"Biome ID: {biome_id}, AC Parameters: {ac_parameters}")
    