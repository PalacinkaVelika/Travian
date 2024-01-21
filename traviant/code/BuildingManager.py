from datetime import datetime, timedelta
from bson import ObjectId

class BuildingManager:
    # Time based building/training 
    def __init__(self,city_manager_instance):
        self._db_collection_name = "building"
        self._collection = None
        self._city_manager = city_manager_instance

    # Create empty record in collection with city_id
    def create_building_record(self, city_id):
        current_datetime = datetime.utcnow()
        new_city_data = {
            "city_id": ObjectId(city_id),
            "building": {
                "building_type": None,
                "time_start": None,
                "time_finish": None
            },
            "army": {
                "soldier_type": None,
                "count": 0, 
                "time_last_checked": None,
                "time_finish": None
            },
            "research": {
                "research_type": None,
                "time_start": None,
                "time_finish": None
            }
        }
        insert_result = self._collection.insert_one(new_city_data)
        if insert_result.inserted_id:
            return True
        return False
    
    # if building is done return True, if it is not done return the time it should finish and what is building
    def check_building_status(self, city_id):
        current_datetime = datetime.utcnow()
        building_stats = self._collection.find_one({"city_id": ObjectId(city_id)})["building"]
        if building_stats["time_finish"] == None:
            return False, 0
        if building_stats["time_finish"] <= current_datetime:
            self.finish_upgrade_building(city_id, building_stats["building_type"])
            return True, 0
        else:
            return False, {building_stats["building_type"]:building_stats["time_finish"]}
    
    # Special version of check_building_status - it checks for status of training soldiers, 
    # update time_last_checked and give the right amount of soldiers to the city        
    def check_soldier_status(self, city_id):
        current_datetime = datetime.utcnow()
        # find record of city_upgrades
        
        # calculate how many bois you already should have - save to var
        
        # add up the var number to city count -> find city of the id and update the value
        
        # update the last checked time value of soldier stuff
        self.update_record(city_id, {
            "$set": {
                "time_last_checked": current_datetime,
            }
        })
    
    def is_building_queue_empty(self, city_id):
        queue = self._collection.find_one({"city_id": ObjectId(city_id)})
        return (queue["building"]["building_type"] == None)

    # Add record of started upgrade
    # upgrade_time should look like this: upgrade_time = timedelta(hours=3, minutes=30, seconds=45)
    def start_upgrade_building(self, city_id, building_type, upgrade_time):
        current_datetime = datetime.utcnow()
        self.update_record(city_id, {
            "$set": {
                "building.building_type": building_type,
                "building.time_start": current_datetime,
                "building.time_finish": current_datetime + upgrade_time
            }
        })
   
   #Logic for upgrading the city building
    def finish_upgrade_building(self, city_id, building_type):
        # increase the building level value by 1
        if(building_type=="coal" or building_type=="ore" or building_type=="energy"):
            print(f"updating level of {building_type}!")
            self._city_manager.update_city_record(city_id, {"$inc": {f"mine_levels.{building_type}": 1}})
        elif(building_type=="academy" or building_type=="machinery" or building_type=="specialists"):
            self._city_manager.update_city_record(city_id, {"$inc": {f"barracks_levels.{building_type}": 1}})
        # reset record of this collection because nothing is upgrading
        self.update_record(city_id, {
            "$set": {
                "building.building_type": None,
                "building.time_start": None,
                "building.time_finish": None
            }
        })
    
    # Add record of started research
    def start_upgrade_research(self, city_id, research_id, upgrade_time):
        current_datetime = datetime.utcnow()
        self.update_record(city_id, {
            "$set": {
                "research.research_type": research_id,
                "research.time_start": current_datetime,
                "research.time_finish": current_datetime + upgrade_time
            }
        })
   
   # Logic for upgrading the city research 
    def finish_upgrade_research(self, city_id, research_id):
        pass
    
    
    # Private function for updating records of this collection
    def update_record(self, city_id, update_operation):
        filter_criteria = {"city_id": ObjectId(city_id)}
        result = self._collection.update_one(filter_criteria, update_operation)
        if result.acknowledged:
            pass
      #      print("Update successful!")
      #      print(f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s).")
      #      print(f"id filter crit. : {ObjectId(city_id)}")
      #  else:
       #     print("Update not acknowledged. filter bad probably lol")
        #    print(f"id filter crit. : {city_id}")
    
    def load_collection(self, database):
        self._collection = database.get_collection(self._db_collection_name)
