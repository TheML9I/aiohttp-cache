from aiohttp_cached import settings
from aiohttp_cached.utils import import_string
from aiohttp_cached.cache.exceptions import InvalidCacheBackendError, ImproperlyConfiguredCacheError
from aiohttp_cached.cache import backends

DEFAULT_CACHE_ALIAS = 'default'

__all__ = (
    'CacheHandler',
)


class CacheHandler:
    """
    A Cache Handler to manage access to Cache instances.
    """

    _caches = {}

    @classmethod
    async def get_cache(cls, alias: str = DEFAULT_CACHE_ALIAS, loop=None) -> backends.AsyncBaseCache:
        try:
            return cls._caches[alias]
        except KeyError:
            pass

        cache = cls._create_cache(alias, loop=loop)
        cls._caches[alias] = await cache.init()

        return cache

    @classmethod
    def _create_cache(cls, alias, loop=None, **kwargs):
        try:
            conf = settings.CACHES[alias]
        except KeyError:
            raise InvalidCacheBackendError("Could not find config for '%s' in settings.CACHES" % alias)

        try:
            try:
                backend = conf['BACKEND']
            except KeyError as e:
                raise ImproperlyConfiguredCacheError("Could not find backend for cache '%s': %s" % (alias, e))
            else:
                params = conf.copy()
                params.update(kwargs)
                backend = params.pop('BACKEND')
                location = params.pop('LOCATION', '')
            backend_cls = import_string(backend)
        except ImportError as e:
            raise InvalidCacheBackendError(
                "Could not find backend '%s': %s" % (backend, e))

        return backend_cls(location, params, loop=loop)
