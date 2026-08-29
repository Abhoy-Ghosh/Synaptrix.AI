import json
import os
import time

BASE_DIR = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
CACHE_FILE = os.path.join(BASE_DIR, "cache.json")
CACHE_TTL = 60 * 60 * 24 * 30  # 30 days


# -----------------------------
# LOAD / SAVE
# -----------------------------
def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_cache(cache):
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


# -----------------------------
# KEY BUILDER
# -----------------------------
def _make_key(topic, mode):
    topic = topic.lower().strip()
    mode = mode or "auto"
    return f"{topic}::{mode}"


# -----------------------------
# GET
# -----------------------------
def get_cached_result(topic, mode=None):
    cache = load_cache()
    key = _make_key(topic, mode)

    entry = cache.get(key)

    if entry is None:
        return None

    # expiry check
    if time.time() - entry["timestamp"] > CACHE_TTL:
        return None

    return entry["data"]


# -----------------------------
# SET
# -----------------------------
def set_cached_result(topic, mode, result):
    cache = load_cache()
    key = _make_key(topic, mode)

    cache[key] = {
        "data": result,
        "timestamp": time.time()
    }

    save_cache(cache)


# -----------------------------
# DELETE
# -----------------------------
def delete_cached_result(topic, mode=None):
    cache = load_cache()

    if mode:
        key = _make_key(topic, mode)
        cache.pop(key, None)
    else:
        # delete all modes for topic
        topic = topic.lower().strip()
        keys_to_delete = [k for k in cache if k.startswith(topic + "::")]
        for k in keys_to_delete:
            cache.pop(k, None)

    save_cache(cache)