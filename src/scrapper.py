import requests
import json
import time
from typing import List, Dict, Optional, Tuple
import os
from dataclasses import dataclass
from geopy import distance
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

@dataclass
class Place:
    name: str
    address: str
    latitude: float
    longitude: float
    place_id: Optional[str] = None
    rating: Optional[float] = None
    types: Optional[List[str]] = None
    opening_hours: Optional[Dict] = None

class PlaceScraper:
    def __init__(self, google_api_key: Optional[str] = None):
        self.google_api_key = google_api_key
        self.geolocator = Nominatim(user_agent="travel_planner")
        
    def get_coordinates_from_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Get coordinates from address using Nominatim (free geocoding service)"""
        try:
            location = self.geolocator.geocode(address)
            if location:
                return (location.latitude, location.longitude)
            return None
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Geocoding error for {address}: {e}")
            return None
    
    def search_places_google(self, query: str, location: Optional[Tuple[float, float]] = None) -> List[Place]:
        """Search places using Google Places API"""
        if not self.google_api_key:
            print("Google API key not provided. Using fallback geocoding.")
            return self._fallback_place_search(query)
        
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'key': self.google_api_key
        }
        
        if location:
            params['location'] = f"{location[0]},{location[1]}"
            params['radius'] = 50000  # 50km radius
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            places = []
            for result in data.get('results', []):
                place = Place(
                    name=result.get('name', ''),
                    address=result.get('formatted_address', ''),
                    latitude=result['geometry']['location']['lat'],
                    longitude=result['geometry']['location']['lng'],
                    place_id=result.get('place_id'),
                    rating=result.get('rating'),
                    types=result.get('types', [])
                )
                places.append(place)
            
            return places
            
        except requests.RequestException as e:
            print(f"Error fetching places from Google: {e}")
            return self._fallback_place_search(query)
    
    def _fallback_place_search(self, query: str) -> List[Place]:
        """Fallback method using Nominatim for place search"""
        try:
            # Try to find the place using Nominatim
            location = self.geolocator.geocode(query)
            if location:
                place = Place(
                    name=query,
                    address=location.address,
                    latitude=location.latitude,
                    longitude=location.longitude
                )
                return [place]
        except Exception as e:
            print(f"Fallback search error: {e}")
        
        return []
    
    def get_place_details_google(self, place_id: str) -> Optional[Dict]:
        """Get detailed information about a place using Google Places API"""
        if not self.google_api_key:
            return None
            
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'key': self.google_api_key,
            'fields': 'opening_hours,rating,reviews,photos'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('result')
        except requests.RequestException as e:
            print(f"Error fetching place details: {e}")
            return None

class TravelPlanner:
    def __init__(self, max_distance_km: float = 50.0):
        self.max_distance_km = max_distance_km
    
    def calculate_distance(self, place1: Place, place2: Place) -> float:
        """Calculate distance between two places in kilometers"""
        coords1 = (place1.latitude, place1.longitude)
        coords2 = (place2.latitude, place2.longitude)
        return distance.geodesic(coords1, coords2).kilometers
    
    def group_nearby_places(self, places: List[Place]) -> List[List[Place]]:
        """Group places that are close to each other"""
        if not places:
            return []
        
        # Sort places by latitude to improve clustering
        sorted_places = sorted(places, key=lambda p: (p.latitude, p.longitude))
        
        groups = []
        used_places = set()
        
        for i, place in enumerate(sorted_places):
            if i in used_places:
                continue
                
            # Start a new group with this place
            current_group = [place]
            used_places.add(i)
            
            # Find nearby places
            for j, other_place in enumerate(sorted_places):
                if j in used_places or i == j:
                    continue
                    
                distance = self.calculate_distance(place, other_place)
                if distance <= self.max_distance_km:
                    current_group.append(other_place)
                    used_places.add(j)
            
            groups.append(current_group)
        
        return groups
    
    def create_travel_plan(self, places: List[Place], max_places_per_day: int = 5) -> Dict[int, List[Place]]:
        """Create a travel plan with places grouped by day"""
        groups = self.group_nearby_places(places)
        
        travel_plan = {}
        day = 1
        
        for group in groups:
            # Split large groups into multiple days if needed
            for i in range(0, len(group), max_places_per_day):
                day_group = group[i:i + max_places_per_day]
                travel_plan[day] = day_group
                day += 1
        
        return travel_plan
    
    def optimize_route(self, places: List[Place]) -> List[Place]:
        """Simple route optimization using nearest neighbor algorithm"""
        if len(places) <= 1:
            return places
        
        unvisited = places.copy()
        route = [unvisited.pop(0)]  # Start with first place
        
        while unvisited:
            current = route[-1]
            nearest = min(unvisited, key=lambda p: self.calculate_distance(current, p))
            route.append(nearest)
            unvisited.remove(nearest)
        
        return route

def main():
    # Example usage
    scraper = PlaceScraper()
    
    # Example places (you can replace these with your own)
    example_places = [
        "Eiffel Tower, Paris",
        "Louvre Museum, Paris", 
        "Notre-Dame Cathedral, Paris",
        "Arc de Triomphe, Paris",
        "Champs-Élysées, Paris",
        "Montmartre, Paris",
        "Sacre-Coeur, Paris",
        "Palace of Versailles, France",
        "Disneyland Paris, France",
        "Château de Fontainebleau, France"
    ]
    
    print("Scraping place coordinates...")
    places = []
    
    for place_name in example_places:
        print(f"Searching for: {place_name}")
        search_results = scraper.search_places_google(place_name)
        if search_results:
            places.extend(search_results)
            print(f"Found: {search_results[0].name} at ({search_results[0].latitude}, {search_results[0].longitude})")
        else:
            print(f"Could not find coordinates for: {place_name}")
        time.sleep(1)  # Be nice to the API
    
    print(f"\nFound {len(places)} places with coordinates")
    
    # Create travel plan
    planner = TravelPlanner(max_distance_km=30.0)
    travel_plan = planner.create_travel_plan(places, max_places_per_day=4)
    
    print("\n=== TRAVEL PLAN ===")
    for day, day_places in travel_plan.items():
        print(f"\nDay {day}:")
        for i, place in enumerate(day_places, 1):
            print(f"  {i}. {place.name} ({place.latitude:.4f}, {place.longitude:.4f})")
        
        # Show distances between places
        if len(day_places) > 1:
            print("  Distances:")
            for i in range(len(day_places) - 1):
                distance = planner.calculate_distance(day_places[i], day_places[i + 1])
                print(f"    {day_places[i].name} → {day_places[i + 1].name}: {distance:.1f} km")

if __name__ == "__main__":
    main()
