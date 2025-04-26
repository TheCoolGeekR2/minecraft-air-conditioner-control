from typing import Dict
from .consts import BIOMES
from .exceptions import BiomeNotFound
from .ac_communicator import AirConditioner

def process_biome(biome_data: Dict, air_conditioner: AirConditioner):
    biome_id = biome_data["biome"]
    biome_name = biome_id.replace("minecraft:", "")
    
    try:
        ac_parameters = BIOMES[biome_name]
    except KeyError:
        raise BiomeNotFound(biome_name)
    
    air_conditioner.update_ac(
        temp=ac_parameters["day_temp"],
        fan_speed=ac_parameters["wind_level"]
    )
