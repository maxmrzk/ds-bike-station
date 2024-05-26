import osmnx as ox
import networkx as nx
import folium
import webbrowser

# Define your source and destination coordinates
src_coords = (34.052235, -118.243683)  # Los Angeles coordinates example
dest_coords = (34.052000, -118.250000)  # Los Angeles coordinates example

# Download the street network data for the area
G = ox.graph_from_point(src_coords, dist=3000, network_type='bike')

# Find the nearest nodes to the source and destination coordinates
src_node = ox.nearest_nodes(G, src_coords[1], src_coords[0])
dest_node = ox.nearest_nodes(G, dest_coords[1], dest_coords[0])

# Calculate the shortest path
route = nx.shortest_path(G, src_node, dest_node, weight='length')

# Extract the latitude and longitude from the route nodes
route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

# Create a folium map
m = folium.Map(location=src_coords, zoom_start=14)

# Add the route to the map
folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=1).add_to(m)

# Add markers for the start and end points
folium.Marker(src_coords, popup='Start', icon=folium.Icon(color='green')).add_to(m)
folium.Marker(dest_coords, popup='End', icon=folium.Icon(color='red')).add_to(m)

# Save the map to an HTML file
file_path = "bike_route_map.html"
m.save(file_path)

# Output the map file path
print("Map has been saved to bike_route_map.html")

webbrowser.open(file_path)
