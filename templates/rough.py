import folium
import requests

# Define the location you want to search for restaurants
location = "London"

# Use the Nominatim API to get the latitude and longitude of the location
url = "https://nominatim.openstreetmap.org/search/" + location + "?format=json"
response = requests.get(url).json()
latitude = response[0]["lat"]
longitude = response[0]["lon"]

# Create a map centered on the location
map = folium.Map(location=[latitude, longitude], zoom_start=15)

# Use the Foursquare API to search for restaurants near the location

# fsq3MtjyQRl+LLz4ig4bosvyvyJx56yzBsxgVwxRr5rp88I=
CLIENT_ID = 'IW3WPCHRNUBWH5KRAXMPT2P3VTKTEWHI2IKRBJFQP50FOGYW'
CLIENT_SECRET = '4JAL0YLBTW5LSMNIAZS0RWTXPXY31NORKYPG43DOIPHCDTNR'
VERSION = '20220318'
LIMIT = 10
radius = 1000
search_query = 'restaurant'

url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(
    CLIENT_ID,
    CLIENT_SECRET,
    latitude,
    longitude,
    VERSION,
    search_query,
    radius,
    LIMIT)

# results = requests.get(url).json()["response"]["venues"]
results = requests.get(url).json()["response"]['venus']

# Add markers to the map to show the location of each restaurant
for result in results:
    name = result["name"]
    lat = result["location"]["lat"]
    lon = result["location"]["lng"]
    marker = folium.Marker([lat, lon], popup=name)
    marker.add_to(map)

# Display the map
# map

map.get_root().render()

