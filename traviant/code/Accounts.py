import bcrypt
from bson import ObjectId
import json

class Accounts:
    #Account management - login, register logic
    def __init__(self):
        self._db_table_name = "accounts"
        self._collection = None

    # If login credentials are correct returns users ID 
    def find_user_id(self, name, password):
        user = self._collection.find_one({"login": name})
        if user:
            if bcrypt.checkpw(password.encode("utf-8"), user["heslo"]):
                 return user["_id"]
        return None
                
    def register_new_user(self, name, password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        register_data = {
                "login" : name,
                "heslo" : hashed_password,
                "score" : 0
        }
        insert_result = self._collection.insert_one(register_data)
        if insert_result.inserted_id:
            return True
        return None
    
    def update_user_score(self, user_id, city_manager_instance):
        calculated_score = 0
        # for each players city add x points
        # for each level of a building in each city add x points 
        for city in city_manager_instance.player_cities(user_id):
            calculated_score += 7
            for mine_level in city["mine_levels"]:
                calculated_score += 4*int(city["mine_levels"][mine_level])
            for barrack_level in city["barracks_levels"]:
                calculated_score += 2*int(city["barracks_levels"][barrack_level])

        filter_criteria = {"_id": ObjectId(user_id)}
        result = self._collection.update_one(filter_criteria, {
            "$set": {
                "score": calculated_score
            }
        })
        if result.acknowledged:
            pass
            print("Update successful!")
            print(f"Matched {result.matched_count} document(s) and modified {result.modified_count} document(s).")
            print(f"id filter crit. : {ObjectId(user_id)}")
        else:
            pass
            print("Update not acknowledged. filter bad probably lol")
            print(f"id filter crit. : {user_id}")
    
    def top_players(self, redis_manager, page_number=1, page_size=10):
        redis_key = f'top_players:{page_number}'
        cached_data = redis_manager.get(redis_key)
        if cached_data:
            data = json.loads(cached_data)
            return data

        skip_value = (page_number - 1) * page_size
        top_players = self._collection.find({}, {'login': 1, 'score': 1, '_id': 0}).sort([('score', -1)]).skip(skip_value).limit(page_size)
        top_players_list = self.redis_json_support(top_players)
        redis_manager.set(redis_key, json.dumps(top_players_list), expiration=3600)
        return top_players_list

    def redis_json_support(self, data):
        return [ {
                'login': record['login'],
                'score': record['score']
            } for record in data]

    def load_collection(self, database):
        self._collection = database.get_collection(self._db_table_name)
