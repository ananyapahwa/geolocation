from flask import Flask, jsonify
import requests
import math

app = Flask(__name__)

# Function to fetch location based on IP
def get_location_by_ip(ip=''):
    url = 'https://ipinfo.io'
    if ip:
        url += f'/{ip}'
    url += '/json'
    response = requests.get(url)
    return response.json()

# Haversine formula to calculate distance between two points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = R * c
    distance_m = distance_km * 1000  # Convert to meters
    return distance_km, distance_m

# Endpoint to get the location and distance
@app.route('/location', methods=['GET'])
def get_location():
    # Fetch location based on IP
    location = get_location_by_ip()
    ip = location.get('ip')
    city = location.get('city')
    region = location.get('region')
    country = location.get('country')
    loc = location.get('loc', '').split(',')
    latitude = float(loc[0]) if loc else 0
    longitude = float(loc[1]) if loc else 0

    # Define the epicenter (example coordinates)
    epicenter_lat = 37.7749  # Example: San Francisco, CA
    epicenter_lon = -122.4194

    # Calculate distance from epicenter
    distance_km, distance_m = haversine(latitude, longitude, epicenter_lat, epicenter_lon)

    # Prepare the response
    result = {
        'ip': ip,
        'city': city,
        'region': region,
        'country': country,
        'latitude': latitude,
        'longitude': longitude,
        'distance_from_epicenter_km': distance_km,
        'distance_from_epicenter_m': distance_m
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
