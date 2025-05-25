# MapSearch class
# This class provides an interactive map widget for searching and displaying nearby food places (restaurants, cafes, fast food)
# using OpenStreetMap data and the Overpass API. It uses TkinterMapView for map display and geopy for geocoding.
#
# Features:
# - Displays a map centered on a given location (default: Patras, Greece).
# - Fetches nearby food places using the Overpass API and displays them as markers.
# - Supports searching for places by name.
# - Limits the number of displayed places for clarity.
# - Implements persistent caching of Overpass API results (in places_cache.json) to speed up repeated searches and reduce API load.
# - All map and place data is displayed inside a given Tkinter/CTkinter frame.
#
# Usage:
#   map_search = MapSearch(parent_frame)
#   map_search.search_location("Athens, Greece", query="pizza")

import requests
from geopy.geocoders import Nominatim
from tkinter import messagebox
import tkintermapview
import json
import hashlib
import os

class MapSearch:
    CACHE_FILE = "places_cache.json"

    def __init__(self, map_placeholder):
        self.map_placeholder = map_placeholder
        self.map_widget = tkintermapview.TkinterMapView(self.map_placeholder, width=800, height=500)
        self.map_widget.pack(fill="both", expand=True)
        self.geolocator = Nominatim(user_agent="myGeocoder")
        self.all_places = []  # Store all places fetched
        self.default_places_shown = 10  # Limit for default places

        # Persistent cache: {cache_key: places}
        self.places_cache = self.load_cache()

        # Initialize the map with Patras, Greece
        self.search_location("Patras, Greece")

    def get_cache_key(self, lat, lon, query, radius):
        key = f"{lat}_{lon}_{query}_{radius}"
        return hashlib.md5(key.encode()).hexdigest()

    def load_cache(self):
        if os.path.exists(self.CACHE_FILE):
            try:
                with open(self.CACHE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_cache(self):
        try:
            with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.places_cache, f)
        except Exception:
            pass  # Ignore cache save errors

    def fetch_nearby_food_places(self, lat, lon, query=None, radius=5000):
        """
        Fetch nearby food places using Overpass API, with persistent caching.
        """
        cache_key = self.get_cache_key(lat, lon, query, radius)
        if cache_key in self.places_cache:
            # Return cached results
            return self.places_cache[cache_key]

        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        node["amenity"~"restaurant|cafe|fast_food"](around:{radius},{lat},{lon});
        out;
        """
        try:
            response = requests.get(overpass_url, params={'data': overpass_query})
            response.raise_for_status()
            data = response.json()

            places = []
            for element in data.get("elements", []):
                name = element.get("tags", {}).get("name", "Unnamed Place")
                if query is None or query.lower() in name.lower():
                    places.append((name, element["lat"], element["lon"]))

            # Save to cache and persist
            self.places_cache[cache_key] = places
            self.save_cache()
            return places
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch places: {e}")
            return []

    def generate_map(self, location, query=None):
        """
        Generate the map for a given location and query.
        """
        loc = self.geolocator.geocode(location)
        if not loc:
            messagebox.showerror("Error", "Location not found.")
            return

        if self.map_widget.winfo_exists():
            self.map_widget.set_position(loc.latitude, loc.longitude)
            self.map_widget.set_zoom(13)
            self.all_places = self.fetch_nearby_food_places(loc.latitude, loc.longitude, query)
            self.show_places(self.all_places[:self.default_places_shown])

    def show_places(self, places):
        """
        Display the given list of places on the map.
        """
        self.map_widget.delete_all_marker()  # Clear existing markers
        for name, lat, lon in places:
            self.map_widget.set_marker(lat, lon, text=name)

    def search_location(self, location, query=None):
        """
        Search for a location and update the map.
        """
        self.generate_map(location, query)
# import requests
# from geopy.geocoders import Nominatim
# from tkinter import messagebox
# import tkintermapview


# class MapSearch:
#     def __init__(self, map_placeholder):
#         self.map_placeholder = map_placeholder
#         self.map_widget = tkintermapview.TkinterMapView(self.map_placeholder, width=800, height=500)
#         self.map_widget.pack(fill="both", expand=True)
#         self.geolocator = Nominatim(user_agent="myGeocoder")
#         self.all_places = []  # Store all places fetched
#         self.default_places_shown = 10  # Limit for default places

#         # Initialize the map with Patras, Greece
#         self.search_location("Patras, Greece")

#     def fetch_nearby_food_places(self, lat, lon, query=None, radius=5000):
#         """
#         Fetch nearby food places using Overpass API.
#         """
#         overpass_url = "http://overpass-api.de/api/interpreter"
#         overpass_query = f"""
#         [out:json];
#         node["amenity"~"restaurant|cafe|fast_food"](around:{radius},{lat},{lon});
#         out;
#         """
#         try:
#             response = requests.get(overpass_url, params={'data': overpass_query})
#             response.raise_for_status()
#             data = response.json()

#             places = []
#             for element in data.get("elements", []):
#                 name = element.get("tags", {}).get("name", "Unnamed Place")
#                 if query is None or query.lower() in name.lower():
#                     places.append((name, element["lat"], element["lon"]))

#             return places
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch places: {e}")
#             return []

#     def generate_map(self, location, query=None):
#         """
#         Generate the map for a given location and query.
#         """
#         loc = self.geolocator.geocode(location)
#         if not loc:
#             messagebox.showerror("Error", "Location not found.")
#             return

#         if self.map_widget.winfo_exists():
#             self.map_widget.set_position(loc.latitude, loc.longitude)
#             self.map_widget.set_zoom(13)
#             self.all_places = self.fetch_nearby_food_places(loc.latitude, loc.longitude, query)
#             self.show_places(self.all_places[:self.default_places_shown])

#     def show_places(self, places):
#         """
#         Display the given list of places on the map.
#         """
#         self.map_widget.delete_all_marker()  # Clear existing markers
#         for name, lat, lon in places:
#             self.map_widget.set_marker(lat, lon, text=name)

#     def search_location(self, location, query=None):
#         """
#         Search for a location and update the map.
#         """
#         self.generate_map(location, query)
