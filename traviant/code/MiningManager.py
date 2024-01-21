from datetime import datetime, timedelta
from bson import ObjectId
from GameLogicData import GameLogicData

class MiningManager:
    # Time based building/training 
    def __init__(self,city_manager_instance):
        self._db_collection_name = "building"
        self._collection = None
        self._city_manager = city_manager_instance

    # Gets data from all mines in a city and adds the correct amount to the storage (key is in calling this at the correct times)
    def mining_update(self, city_id):
        # Get data from city mine levels
        city_data = self._city_manager.one_city_by_id(city_id)
        coal_level = city_data["mine_levels"]["coal"]
        ore_level = city_data["mine_levels"]["ore"]
        energy_level = city_data["mine_levels"]["energy"]
        # Calculate amount added -> base amount * bonus
        logic_data = GameLogicData().building_levels
        coal_amount = logic_data["coal"]["base_production_speed"] * logic_data["coal"][str(coal_level)]["production_speed_bonus"] if coal_level > 0 else 0
        ore_amount = logic_data["ore"]["base_production_speed"] * logic_data["ore"][str(ore_level)]["production_speed_bonus"] if ore_level > 0 else 0
        energy_amount = logic_data["energy"]["base_production_speed"] * logic_data["energy"][str(energy_level)]["production_speed_bonus"] if energy_level > 0 else 0
        # Add the amount
        self._city_manager.update_city_record(city_id, {
            "$inc": {
                "resources.coal": coal_amount,
                "resources.ore": ore_amount,
                "resources.energy": energy_amount
            
            }
        })
    
    
    def load_collection(self, database):
        self._collection = database.get_collection(self._db_collection_name)
