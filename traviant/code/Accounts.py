import bcrypt

class Accounts:
    def __init__(self):
        self._db_table_name = "accounts"
        self._account_collection = None

    def login_user(self, name, password):
        user = self._account_collection.find_one({"login": name})
        if user:
            if bcrypt.checkpw(password.encode("utf-8"), user["heslo"]):
                return True
                
    def register_new_user(self, name, password):
        ...
    
    def load_collection(self, database):
        self._account_collection = database.get_collection(self._db_table_name)
