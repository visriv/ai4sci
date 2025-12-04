from diskcache import Cache
import hashlib
import json

cache = Cache("cache/")

def _hash(data: dict) -> str:
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def cache_get(key_obj: dict):
    key = _hash(key_obj)
    return cache.get(key)

def cache_set(key_obj: dict, value):
    key = _hash(key_obj)
    cache.set(key, value, expire=60*60)  # 1 hour TTL
