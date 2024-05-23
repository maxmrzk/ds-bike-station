import pandas as pd
import requests
from geopy.distance import geodesic


def find_nearest_stations(K, current_location):
    url = 'https://bikeshare.metro.net/stations/json/'

    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        data = None
    except ValueError as e:
        print(f"JSON decode error: {e}")
        data = None

    if data:
        features = data['features']

        stations = []

        for feature in features:
            properties = feature['properties']
            coordinates = feature['geometry']['coordinates']
            station_info = {
                'name': properties['name'],
                'latitude': coordinates[1],
                'longitude': coordinates[0],
                'bikesAvailable': properties['bikesAvailable']
            }
            stations.append(station_info)

        df = pd.DataFrame(stations)

        def calculate_distance(lat1, lon1, lat2, lon2):
            return geodesic((lat1, lon1), (lat2, lon2)).kilometers

        df['distance'] = df.apply(lambda row: calculate_distance(current_location[0],
                                                                 current_location[1],
                                                                 row['latitude'],
                                                                 row['longitude']), axis=1)

        nearest_stations = df.sort_values(by='distance').head(K)

        print(nearest_stations[['name', 'latitude', 'longitude', 'distance', 'bikesAvailable']])
    else:
        print("No Data available")
