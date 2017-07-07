class AsyncBaseCache:
    def __init__(self, location, params, loop=None):
        self._params = params
        self._location = location
        self._loop = loop

        self._key_prefix = self._params.get('PREFIX', '')

    async def init(self, *args, **kwargs):
        return self

    async def get(self, key: str, default=None):
        raise NotImplementedError('subclasses of AsyncBaseCache must provide a get() method')

    async def set(self, key: str, value, timeout=1):
        raise NotImplementedError('subclasses of AsyncBaseCache must provide a set() method')

    async def delete(self, key: str):
        raise NotImplementedError('subclasses of AsyncBaseCache must provide a delete() method')

    async def has(self, key: str) -> bool:
        return self.get(key) is not None

    async def clear(self):
        raise NotImplementedError('subclasses of AsyncBaseCache must provide a clear() method')

    async def close(self):
        raise NotImplementedError('subclasses of AsyncBaseCache must provide a close() method')

    def build_key(self, key):
        return '%s_%s' % (self._key_prefix, key)
