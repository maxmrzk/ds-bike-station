import pandas as pd
import requests
from geopy.distance import geodesic


def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers


url = 'https://bikeshare.metro.net/stations/json/'

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def find_nearest_stations(K, current_location):

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

        # Extract the relevant data from the Response object
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
        # Convert Data to Pandas Data Frame
        df = pd.DataFrame(stations)

        # Calculate the distance between each user and the bike stations
        df['distance'] = df.apply(lambda row: calculate_distance(current_location[0],
                                                                 current_location[1],
                                                                 row['latitude'],
                                                                 row['longitude']), axis=1)
        # Sort the results in ascending order and cut for K
        nearest_stations = df.sort_values(by='distance').head(K)

        print(nearest_stations[['name', 'latitude', 'longitude', 'distance', 'bikesAvailable']])
        return nearest_stations
    else:
        print("No Data available")
        return None


def find_nearest_stations_with_available_docks(K, current_location):

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
                'docksAvailable': properties['docksAvailable']
            }
            stations.append(station_info)

        df = pd.DataFrame(stations)

        df = df[df['docksAvailable'] > 0]

        df['distance'] = df.apply(
            lambda row: calculate_distance(current_location[0], current_location[1], row['latitude'], row['longitude']),
            axis=1)

        nearest_stations = df.sort_values(by='distance').head(K)

        print(nearest_stations[['name', 'latitude', 'longitude', 'distance', 'docksAvailable']])
        return nearest_stations
    else:
        print("No data available")
