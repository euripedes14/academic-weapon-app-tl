import requests
from geopy.geocoders import Nominatim
from tkinter import messagebox
import tkintermapview

class MapSearch:
    def __init__(self, map_placeholder):
        self.map_placeholder = map_placeholder
        self.map_widget = tkintermapview.TkinterMapView(self.map_placeholder, width=800, height=500)
        self.map_widget.pack(fill="both", expand=True)
        self.geolocator = Nominatim(user_agent="myGeocoder")
        self.all_places = []  # Store all places fetched
        self.default_places_shown = 10  # Limit for default places

        # Bind zoom event to dynamically load more places
        self.map_widget.bind("<ButtonRelease-1>", self.on_map_zoom)

    def fetch_nearby_food_places(self, lat, lon, query=None, radius=5000):
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

    def generate_map(self, location, query=None):
        loc = self.geolocator.geocode(location)
        if not loc:
            messagebox.showerror("Error", "Location not found.")
            return

        self.map_widget.set_position(loc.latitude, loc.longitude)
        self.map_widget.set_zoom(13)

        # Fetch all places and store them
        self.all_places = self.fetch_nearby_food_places(loc.latitude, loc.longitude, query)

        # Show only the first 50 places by default
        self.show_places(self.all_places[:self.default_places_shown])

    def show_places(self, places):
        """Display the given list of places on the map."""
        self.map_widget.delete_all_marker()  # Clear existing markers
        for name, lat, lon in places:
            self.map_widget.set_marker(lat, lon, text=name)

    def on_map_zoom(self, event):
        """Load more places as the user zooms into the map."""
        zoom_level = self.map_widget.zoom
        if zoom_level > 20:  # Adjust the zoom level threshold as needed
            # Show all places if zoomed in enough
            self.show_places(self.all_places)
        else:
            # Show only the default number of places
            self.show_places(self.all_places[:self.default_places_shown])

    def search_location(self, location, query=None):
        self.generate_map(location, query)