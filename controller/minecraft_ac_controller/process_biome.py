from typing import Dict
from .consts import BIOMES
from .exceptions import BiomeNotFound
from .ac_communicator import AirConditioner

def process_biome(data: Dict, air_conditioner: AirConditioner):
    biome_parameters = BIOMES[data['biome'].replace("minecraft:", "")]
    temperature = biome_parameters["day_temp"] if data["time_of_day"] == 'DAY' else biome_parameters["night_temp"]
    air_conditioner.update_ac(
        temp=temperature,
        fan_speed=biome_parameters["wind_level"] * 5
    )
