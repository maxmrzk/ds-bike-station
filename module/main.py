from calc import find_nearest_stations
from calc import find_nearest_stations_with_available_docks


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

    find_nearest_stations(K, current_location)
    find_nearest_stations_with_available_docks(K, current_location)


if __name__ == "__main__":
    main()
