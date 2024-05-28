import folium


def create_map(user_coords, stations_df):
    # Check if stations_df is None or empty
    if stations_df is None or stations_df.empty:
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

    # Add markers for the nearest bike stations
    for _, station in stations_df.iterrows():
        folium.Marker(
            location=[station['latitude'], station['longitude']],
            popup=f"{station['name']}<br>Bikes Available: {station['bikesAvailable']}<br>Distance: {station['distance']:.2f} km",
            icon=folium.Icon(color='green', icon='bicycle', prefix='fa')
        ).add_to(map_)

    # Return the map object
    return map_