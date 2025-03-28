import requests
from geopy.geocoders import Nominatim
from tkinter import messagebox
import tkintermapview

def fetch_nearby_food_places(lat, lon, query=None, radius=5000):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    node["amenity"~"restaurant|cafe|fast_food"](around:{radius},{lat},{lon});
    out;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    
    places = []
    for element in data.get("elements", []):
        name = element.get("tags", {}).get("name", "Unnamed Place")
        if query is None or query.lower() in name.lower():
            places.append((name, element["lat"], element["lon"]))
    
    return places

def generate_map(map_placeholder, location, query=None):
    map_widget = tkintermapview.TkinterMapView(map_placeholder, width=800, height=500)
    map_widget.pack(fill="both", expand=True)
    
    geolocator = Nominatim(user_agent="myGeocoder")
    loc = geolocator.geocode(location)
    if not loc:
        messagebox.showerror("Error", "Location not found.")
        return
    
    map_widget.set_position(loc.latitude, loc.longitude)
    map_widget.set_zoom(13)
    
    food_places = fetch_nearby_food_places(loc.latitude, loc.longitude, query)
    for name, lat, lon in food_places:
        map_widget.set_marker(lat, lon, text=name)

def search_location(map_placeholder, location, query=None):
    generate_map(map_placeholder, location, query)