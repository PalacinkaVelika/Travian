import redis
from flask import current_app

class RedisManager:
    def __init__(self):
        self.redis = redis.Redis(host=current_app.config['REDIS_HOST'], port=current_app.config['REDIS_PORT'])

    def set(self, key, value, expiration=None):
        return self.redis.set(key, value, ex=expiration)

    def get(self, key):
        return self.redis.get(key)

    def exists(self, key):
        return self.redis.exists(key)