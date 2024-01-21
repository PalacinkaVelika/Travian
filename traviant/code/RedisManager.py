import redis

class RedisManager:
    def __init__(self, app=None):
        self.redis = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.redis = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])

    def set(self, key, value, expiration=None):
        return self.redis.set(key, value, ex=expiration)

    def get(self, key):
        return self.redis.get(key)

    def exists(self, key):
        return self.redis.exists(key)
    
    def flush_db(self):
        # Flush the entire database
        return self.redis.flushdb()