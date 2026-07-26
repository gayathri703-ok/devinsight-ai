import time

_cache: dict[str, dict] = {}
CACHE_TTL_SECONDS = 600  # 10 minutes


def get_cached(key: str):
    entry = _cache.get(key)
    if entry is None:
        return None

    if time.time() - entry["timestamp"] > CACHE_TTL_SECONDS:
        del _cache[key]
        return None

    return entry["data"]


def set_cached(key: str, data: dict):
    _cache[key] = {
        "data": data,
        "timestamp": time.time(),
    }