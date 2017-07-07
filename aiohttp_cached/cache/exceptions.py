from aiohttp_cached import exceptions


class InvalidCacheBackendError(exceptions.ImproperlyConfigured):
    pass


class ImproperlyConfiguredCacheError(exceptions.ImproperlyConfigured):
    pass
