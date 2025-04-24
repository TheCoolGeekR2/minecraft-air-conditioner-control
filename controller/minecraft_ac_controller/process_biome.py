from typing import Dict
from .consts import BIOMES

def process_biome(biome_data: Dict):
    biome_id = biome_data["biome"]
    biome_name = biome_id.replace("minecraft:", "")
    ac_parameters = BIOMES[biome_name]
    print(f"Biome ID: {biome_id}, AC Parameters: {ac_parameters}")
    
