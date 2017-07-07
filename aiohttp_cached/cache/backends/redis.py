import aioredis
import pickle

from aiohttp_cached.exceptions import ImproperlyConfigured
from aiohttp_cached.cache.backends import AsyncBaseCache

__all__ = (
    'RedisCache',
)


class RedisCache(AsyncBaseCache):
    def __init__(self, location: str, params: dict, loop=None):
        super().__init__(location, params, loop=loop)

        self._host = None
        self._db = None
        self._pool = None

    async def init(self):
        """
        Must be invoked after class instantiation to process object properties asynchronously
        :return: Redis cache object
        :rtype: RedisCache
        """
        self.init_connection_params()
        self._pool = await self._create_pool()

        return self

    async def _create_pool(self):
        return await aioredis.create_pool(self._host, db=self._db, loop=self._loop,
                                          **self._params.get('OPTIONS', {}))

    def init_connection_params(self):
        if ':' in self._location:
            try:
                _host, _port, _db = self._location.split(':')
            except ValueError:
                raise ImproperlyConfigured("Host, port and database or unix \
                                            socked path must be specified (e.g. localhost:6379:1).")
            try:
                _port = int(_port)
                _db = int(_db)
            except (ValueError, TypeError):
                raise ImproperlyConfigured("Port and db values must be an integer.")

            self._host = (_host, _port)
            self._db = _db
        else:
            self._host = self._location  # unix socket path
            self._db = self._params.get('DB', 0)

    async def get(self, key: str, default=None):
        async with self._pool.get() as redis:
            redis_value = await redis.get(self.build_key(key))

            if redis_value is None:
                return default

            try:
                result = int(redis_value)
            except (ValueError, TypeError):
                result = self.unpack_object(redis_value)

            return result

    async def set(self, key: str, value, timeout: int = 0):
        packed_obj = self.pack_object(value)

        async with self._pool.get() as redis:
            await redis.set(self.build_key(key), packed_obj, expire=timeout)

    async def delete(self, key: str):
        async with self._pool.get() as redis:
            await redis.delete(self.build_key(key))

    async def has(self, key: str) -> bool:
        async with self._pool.get() as redis:
            return await redis.exists(self.build_key(key))

    async def clear(self):
        async with self._pool.get() as redis:
            if self._key_prefix:
                _keys = await redis.keys('%s*' % self._key_prefix)

                if _keys:
                    await redis.delete(*_keys)
            else:
                await redis.flushdb()

    async def close(self):
        pass

    def unpack_object(self, value):
        if isinstance(value, memoryview):
            return bytes(value)

        try:
            return pickle.loads(value)
        except TypeError:
            return None

    def pack_object(self, value):
        return pickle.dumps(value)
