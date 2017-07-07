from functools import wraps

from aiohttp_cached.cache import CacheHandler, DEFAULT_CACHE_ALIAS


def cache(key, enabled: bool=True, backend=DEFAULT_CACHE_ALIAS, timeout=None):
    def decorator(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            if enabled:
                cache_backend = await CacheHandler.get_cache(backend)
                _key = key if not callable(key) else key(*args, **kwargs)

                result = await cache_backend.get(_key)

                if result is not None:
                    return result

            result = await func(*args, **kwargs)

            if enabled:
                await cache_backend.set(_key, result, timeout=timeout)

            return result

        return wrapped

    return decorator
