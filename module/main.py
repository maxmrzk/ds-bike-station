from calc import find_nearest_stations
from calc import find_nearest_stations_with_available_docks
from module.gui import create_map


def main():
    while True:
        try:
            K = int(input("Enter the number of nearest bike stations to find (K): "))
            if K > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    current_location = (34.0522, -118.2437)
    print(f"Your Location: {current_location}")

    stations_df = find_nearest_stations(K, current_location)
    docks_df = find_nearest_stations_with_available_docks(K, current_location)

    if stations_df.any:
        user_bike_map = create_map(current_location, stations_df)
        user_bike_map.save('user_bike_map.html')

    if docks_df.any:
        dock_map = create_map(current_location, docks_df)
        dock_map.save('user_dock_map.html')


if __name__ == "__main__":
    main()
