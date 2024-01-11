import random
from bson import ObjectId
from bson.json_util import loads, dumps
 
class City:
    # Loading city, Upgrading buildings, adding soldiers to citys army, adding resources to citys resources
    def __init__(self):
        self._db_table_name = "cities"
        self._account_collection = None
        self.x_max = 16
        self.region_max = 10

    # Creates new city in database on the set coordinates
    def create_new_city(self, region, x, owner_id):
        if (self.one_city(region, x) == None):
            new_city_data = {
                "owner" : owner_id,
                "position": {
                    "region": region,
                    "x": x
                },
                "resources": {
                    "coal": 0,
                    "ore": 0,
                    "energy": 0
                },
                "mine_levels": {
                    "coal": 0,
                    "ore": 0,
                    "energy": 0
                },
                "barracks_levels": {
                    "academy": 0,
                    "machinery": 0,
                    "specialists": 0
                },
                "army": {
                    "soldier": {
                        "lvl": 0,
                        "count": 0
                    },
                    "tank": {
                        "lvl": 0,
                        "count": 0
                    },
                    "anti-tank": {
                        "lvl": 0,
                        "count": 0
                    }
                }
            }
            insert_result = self._account_collection.insert_one(new_city_data)
            if insert_result.inserted_id:
                return True
            return False
        return False

    # Create City on random unclaimed coordinates
    def create_random_city(self, owner_id):
        region = random.randint(0, self.region_max)
        x = random.randint(0, self.x_max)
        #Check if city with the coords exist
        if (self.one_city(region, x) == None):  
            self.create_new_city(region, x, owner_id)
        else: 
            self.create_random_city(owner_id)

    def one_city(self, region, x):
        city = self._account_collection.find_one({"position":{"region": region, "x": x}})
        if city:
            city = loads(dumps(city))
        return city

    def player_cities(self, owner_id):
        cities_cursor = self._account_collection.find({"owner": ObjectId(owner_id)})
        '''
        cities_list = list(cities_cursor)
        for city in cities_cursor:
             for key, value in record.items():
                if isinstance(value, ObjectId):
                    record[key] = str(value)
        print(cities_list)
        '''
        return cities_list
    
    def region_cities(self, region):
        cities_cursor = self._account_collection.find({"position.region": region})
        cities_list = [loads(dumps(city)) for city in cities_cursor]
        return cities_list

       
    def load_collection(self, database):
        self._account_collection = database.get_collection(self._db_table_name)