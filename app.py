from flask import Flask, render_template, jsonify
import json, os

app = Flask(__name__)

# Load hotels data (merged with restaurants + sightseeing)
json_path = os.path.join(app.root_path, "static", "hotels-merged.json")
try:
    with open(json_path, "r", encoding="utf-8") as f:
        HOTELS = json.load(f)
except Exception as e:
    HOTELS = []
    print(f"❌ Failed to load hotels: {e}")

# API: all hotels
@app.route("/api/hotels")
def hotels_api():
    return jsonify(HOTELS)

# API: city guide
@app.route("/api/guide/<city>")
def guide(city):
    city_hotels = [h for h in HOTELS if h.get("city", "").lower() == city.lower()]
    if not city_hotels:
        return jsonify({"restaurants": [], "sightseeing": []})

    restaurants = []
    sightseeing = []
    for h in city_hotels:
        restaurants.extend(h.get("restaurants", []))
        sightseeing.extend(h.get("sightseeing", []))

    restaurants = list(set(restaurants))
    sightseeing = list(set(sightseeing))

    restaurants_with_links = [
        {"name": r, "maps_url": f"https://www.google.com/maps/search/?api=1&query={r.replace(' ', '+')}"}
        for r in restaurants
    ]
    sightseeing_with_links = [
        {"name": s, "maps_url": f"https://www.google.com/maps/search/?api=1&query={s.replace(' ', '+')}"}
        for s in sightseeing
    ]

    return jsonify({
        "restaurants": restaurants_with_links,
        "sightseeing": sightseeing_with_links
    })

# Homepage
@app.route("/")
def home_page():
    return render_template("index.html")

# Hotels page
@app.route("/hotels")
def hotels_page():
    return render_template("hotels.html")

if __name__ == "__main__":
    app.run(debug=True)
