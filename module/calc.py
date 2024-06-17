import pandas as pd
import requests
from geopy.distance import geodesic
import folium


def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers


url = 'https://bikeshare.metro.net/stations/json/'

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def find_nearest_stations(k, current_location):

    if not k > 0:
        return

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
            if station_info['bikesAvailable'] > 0:
                stations.append(station_info)

        # Convert Data to Pandas Data Frame
        df = pd.DataFrame(stations)

        # Calculate the distance between each user and the bike stations
        df['distance'] = df.apply(lambda row: calculate_distance(current_location[0],
                                                                 current_location[1],
                                                                 row['latitude'],
                                                                 row['longitude']), axis=1)
        # Sort the results in ascending order and cut for K
        nearest_stations = df.sort_values(by='distance').head(k)

        print(nearest_stations[['name', 'latitude', 'longitude', 'distance', 'bikesAvailable']])
        return nearest_stations
    else:
        print("No Data available")
        return None


def find_nearest_stations_with_available_docks(k, current_location):

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
            if station_info['docksAvailable'] > 0:
                stations.append(station_info)

        df = pd.DataFrame(stations)

        df['distance'] = df.apply(
            lambda row: calculate_distance(current_location[0], current_location[1], row['latitude'], row['longitude']),
            axis=1)

        nearest_stations = df.sort_values(by='distance').head(k)

        print(nearest_stations[['name', 'latitude', 'longitude', 'distance', 'docksAvailable']])
        return nearest_stations
    else:
        print("No data available")


def find_route(source_location, destination_location):
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

        stations_df = pd.DataFrame(stations)

        # Use a API for proper routing
        ors_api_key = 'YOUR_API_KEY'

        # Find closest stations to source and destination
        source_station = find_closest_station(source_location, stations_df, need_bikes=True)
        destination_station = find_closest_station(destination_location, stations_df, need_bikes=False)

        # Create a folium map centered at the source location
        map_center = source_location
        bike_map = folium.Map(location=map_center, zoom_start=15)
        folium.Marker(source_location, tooltip='Starting Point',
                      icon=folium.Icon(color='blue', icon='user')).add_to(bike_map)

        # Add marker for the destination
        folium.Marker(destination_location, tooltip='Destination', icon=folium.Icon(color='red', icon='user')).add_to(bike_map)

        # Add logic based on whether the source and destination stations are the same
        if source_station['name'] == destination_station['name']:
            # Plot walking route from source to destination
            folium.PolyLine([source_location, destination_location], color='blue', weight=5,
                            tooltip='Walking Route').add_to(bike_map)
        else:
            # Mark source and destination stations
            folium.Marker((source_station['latitude'], source_station['longitude']),
                          tooltip=source_station['name'], icon=folium.Icon(color='green', icon='bicycle',
                                                                           prefix='fa')).add_to(bike_map)
            folium.Marker((destination_station['latitude'], destination_station['longitude']),
                          tooltip=destination_station['name'], icon=folium.Icon(color='orange', icon='bicycle',
                                                                                prefix='fa')).add_to(bike_map)

            # Get biking route from sourceStation to destinationStation
            biking_route = get_route(ors_api_key,
                                     (source_station['latitude'], source_station['longitude']),
                                     (destination_station['latitude'], destination_station['longitude']),
                                     mode='cycling-regular')
            folium.GeoJson(biking_route, name='Biking Route', style_function=lambda x: {'color': 'red'}).add_to(bike_map)

            # Get walking route from source to sourceStation
            walk_to_station_route = get_route(ors_api_key, source_location,
                                              (source_station['latitude'], source_station['longitude']),
                                              mode='foot-walking')
            folium.GeoJson(walk_to_station_route, name='Walking Route to Station').add_to(bike_map)

            # Get walking route from destinationStation to destination
            walk_from_station_route = get_route(ors_api_key,
                                                (destination_station['latitude'], destination_station['longitude']),
                                                destination_location,
                                                mode='foot-walking')
            folium.GeoJson(walk_from_station_route, name='Walking Route from Station').add_to(bike_map)

        # Save the map to an HTML file and open it in the browser
        bike_map.save('views/distance_map.html')


def find_closest_station(location, stations_df, need_bikes=True):
    def available(row):
        if need_bikes:
            return row['bikesAvailable'] > 0
        else:
            return True

    distances = stations_df.apply(
        lambda row: geodesic(location, (row['latitude'], row['longitude'])).meters, axis=1
    )
    stations_df['distance'] = distances
    filtered_stations = stations_df[stations_df.apply(available, axis=1)]
    closest_station = filtered_stations.loc[filtered_stations['distance'].idxmin()]
    return closest_station

# Function to get route from OpenRouteService API
def get_route(api_key, start, end, mode='foot-walking'):
    url = f"https://api.openrouteservice.org/v2/directions/{mode}/geojson"
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": [[start[1], start[0]], [end[1], end[0]]]
    }
    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching route: {response.status_code}")
        return None

    route_data = response.json()

    if 'features' not in route_data:
        print("Invalid GeoJSON format received.")
        return None

    return route_data