import json
import requests
from redis import Redis

# Redis
redis = Redis(
    host="redis",
    port=6379,
    decode_responses=True,
)

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=-22.2758&longitude=166.4579"
    "&current=temperature_2m,wind_speed_10m,cloud_cover_low,rain"
    "&timezone=Pacific/Noumea"
)

CACHE_TTL = 300  # 5 minutes


def get_current_weather() -> dict:
    """
    Retourne uniquement la météo actuelle (température, vent, nuages, pluie).
    Mise en cache Redis.
    """
    cache_key = "weather_current"
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)

    resp = requests.get(WEATHER_URL, timeout=10)
    resp.raise_for_status()
    raw = resp.json()

    current = raw.get("current", {})
    result = {
        "time": current.get("time"),
        "temperature": current.get("temperature_2m", "—"),
        "wind": current.get("wind_speed_10m", "—"),
        "clouds": current.get("cloud_cover_low", "—"),
        "rain": current.get("rain", "—"),
    }

    redis.set(cache_key, json.dumps(result), ex=CACHE_TTL)
    return result
