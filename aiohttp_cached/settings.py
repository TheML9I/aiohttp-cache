PROJECT_HOST = 'localhost'
PROJECT_PORT = 8023

CACHES = {
    'default': {
        'BACKEND': 'aiohttp_cached.cache.backends.redis.RedisCache',
        'LOCATION': 'localhost:6379:0',
        'OPTIONS': {},
        'PREFIX': '',
    }
}
