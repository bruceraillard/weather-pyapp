import os
from datetime import datetime
from flask import Flask, render_template, jsonify, make_response
from redis import Redis, exceptions as redis_exceptions
from services.weather_service import get_current_weather

app = Flask(__name__)

# Redis (config simple)
redis = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
    socket_timeout=1.0,
)


@app.route("/")
def index():
    # Compteur de visites
    try:
        visits = redis.incr("hits")
    except redis_exceptions.RedisError:
        visits = 0

    try:
        weather = get_current_weather()
    except Exception as e:
        app.logger.error(f"Weather error: {e}")
        weather = None

    return render_template(
        "index.html",
        visits=visits,
        weather=weather,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


@app.route("/api/weather")
def api_weather():
    try:
        weather = get_current_weather()
        resp = make_response(jsonify(weather))
        resp.headers["Cache-Control"] = "public, max-age=60"
        return resp
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
