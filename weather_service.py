import requests
import redis
from datetime import timedelta

r = redis.Redis(host='redis', port=6379)

def get_weather():
    cache_key = "temp_noumea"
    cached = r.get(cache_key)

    if cached:
        try:
            return float(cached.decode("utf-8"))
        except Exception:
            pass

    url = "https://api.open-meteo.com/v1/forecast?latitude=-22.2758&longitude=166.4579&current=temperature_2m&timezone=Pacific/Noumea"

    try:
        response = requests.get(url)
        data = response.json()
        temperature = data["current"]["temperature_2m"]
        r.setex(cache_key, timedelta(minutes=10), str(temperature))
        return float(temperature)
    except Exception as e:
        print("Erreur dans get_weather:", e)
        return None

