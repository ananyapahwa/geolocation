from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Define the epicenter coordinates
epicenter_lat = 30.33625000  # Latitude of New Delhi
epicenter_lon =76.39220000  # Longitude of New Delhi

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = R * c
    distance_m = distance_km * 1000  # Convert km to meters
    return distance_km, distance_m

@app.route('/')
def home():
    return "Hello, World!"  # Basic route for testing

@app.route('/distance', methods=['POST'])
def get_distance():
    if not request.is_json:
        return jsonify({"error": "Invalid input, JSON expected"}), 400

    data = request.get_json()

    if 'lat' not in data or 'lon' not in data:
        return jsonify({"error": "Missing 'lat' or 'lon' in request"}), 400

    try:
        current_lat = float(data['lat'])
        current_lon = float(data['lon'])
    except ValueError:
        return jsonify({"error": "Invalid latitude or longitude values"}), 400

    distance_km, distance_m = calculate_distance(epicenter_lat, epicenter_lon, current_lat, current_lon)
    return jsonify({"distance_km": distance_km, "distance_m": distance_m})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
