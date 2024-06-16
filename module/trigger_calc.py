import folium
from enum import Enum

from calc import find_nearest_stations
from calc import find_nearest_stations_with_available_docks


# sample coordinates 34.0522, -118.2437

class Mode(Enum):
    BIKES = 1
    DOCKS = 2
    DISTANCE = 3


def get_coordinates():
    try:
        # Prompt the user for input
        latitude = float(input("Enter latitude (-90 to 90): "))
        longitude = float(input("Enter longitude (-180 to 180): "))

        # Validate the input values
        if not (-180 <= longitude <= 180):
            raise ValueError(f"Invalid longitude value: {longitude}. Must be between -180 and 180.")
        if not (-90 <= latitude <= 90):
            raise ValueError(f"Invalid latitude value: {latitude}. Must be between -90 and 90.")

        print(f"Valid coordinates: Longitude = {longitude}, Latitude = {latitude}")
        return latitude, longitude
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    while True:
        print("To find the nearest bike sharing stations type: 1")
        print("To find the nearest docking stations type: 2")
        print("To find the shortest route between source and destination type: 3")
        print("To exit the program enter any other value")
        mode = int(input("Enter the number of the mode you want to use: "))
        if mode == 1 or mode == 2:
            try:
                k = int(input("Enter the number of nearest bike stations to find (K): "))
                if k < 0:
                    print("Please enter a positive integer")
                    break

                coordinates = get_coordinates()
                if mode == 1:
                    trigger_station_calc(k, coordinates)
                else:
                    trigger_dock_calc(k, coordinates)
            except ValueError:
                print("Invalid input. Please enter a positive integer.")

        elif mode == 3:
            print("Enter coordinates for source location")
            src_location = get_coordinates()
            print("Enter coordinates for destination location")
            destination = get_coordinates()
            trigger_distance_calc(src_location, destination)
        else:
            break


def trigger_station_calc(k, coord):
    stations_df = find_nearest_stations(k, coord)
    if stations_df.any:
        user_bike_map = create_map(coord, stations_df, Mode.BIKES)
        user_bike_map.save('user_bike_map.html')


def trigger_dock_calc(k, coord):
    docks_df = find_nearest_stations_with_available_docks(k, coord)
    if docks_df.any:
        dock_map = create_map(coord, docks_df, Mode.DOCKS)
        dock_map.save('user_dock_map.html')


def trigger_distance_calc(source, destination):
    print("TODO")


def create_map(user_coords, result_df, mode):
    # Check if stations_df is None or empty
    if result_df is None or result_df.empty:
        raise ValueError("The stations DataFrame is None or empty")

    # Create a Folium map centered around the user's location
    user_lat, user_lon = user_coords
    map_ = folium.Map(location=[user_lat, user_lon], zoom_start=15)

    # Add a marker for the user's location
    folium.Marker(
        location=[user_lat, user_lon],
        popup='User Location',
        icon=folium.Icon(color='blue', icon='user', prefix='fa')
    ).add_to(map_)

    if mode == Mode.BIKES:
        # Add Markers for Task1, nearest bike station
        for _, station in result_df.iterrows():
            folium.Marker(
                location=[station['latitude'], station['longitude']],
                popup=f"{station['name']}<br>Bikes Available: {station['bikesAvailable']}<br>Distance: {station['distance']:.2f} km",
                icon=folium.Icon(color='green', icon='bicycle', prefix='fa')
            ).add_to(map_)
    elif mode == Mode.DOCKS:
        # Add Markers for Task2, nearest docking station
        for _, station in result_df.iterrows():
            folium.Marker(
                location=[station['latitude'], station['longitude']],
                popup=f"{station['name']}<br>Docks Available: {station['docksAvailable']}<br>Distance: {station['distance']:.2f} km",
                icon=folium.Icon(color='green', icon='bolt', prefix='fa')
            ).add_to(map_)
    elif mode == Mode.DISTANCE:
        # Add a marker for target location
        for _, destination in result_df.iterrows():
            folium.Marker(
                location=[destination['latitude'], destination['longitude']],
                popup=f"{destination['distance']:.2f} km",
                icon=folium.Icon(color='green', icon='location', prefix='fa')
            ).add_to(map_)

    # Return the map object
    return map_


if __name__ == '__main__':
    main()
