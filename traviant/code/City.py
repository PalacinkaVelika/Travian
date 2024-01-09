
class City:
    # Loading city, Upgrading buildings, adding soldiers to citys army, adding resources to citys resources
    def __init__(self):
        self._db_table_name = "cities"
        self._account_collection = None

    # Creates new city in database on the set coordinates
    def create_new_city(self, region, x):
        if (self.one_city(region, x) == None):
            new_city_data = {
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

    def one_city(self, region, x):
        city = self._account_collection.find_one({"position":{"region": region, "x": x}})
        return city
       
    def region_cities(self, region):
        cities = self._account_collection.find({"position.region": region})
        return cities

       
    def load_collection(self, database):
        self._account_collection = database.get_collection(self._db_table_name)