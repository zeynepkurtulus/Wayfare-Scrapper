#!/usr/bin/env python3
"""
Example usage of the Travel Planner API
Demonstrates how to use the scraper and planner programmatically
"""

from wayfare_scrapper import PlaceScraper, TravelPlanner, Place
import json

def example_basic_usage():
    """Basic example of using the travel planner"""
    print("=== Basic Travel Planning Example ===\n")
    
    # Initialize scraper and planner
    scraper = PlaceScraper()
    planner = TravelPlanner(max_distance_km=25.0)
    
    # Define places to visit
    places_to_visit = [
        "Times Square, New York",
        "Central Park, New York", 
        "Empire State Building, New York",
        "Brooklyn Bridge, New York",
        "Statue of Liberty, New York"
    ]
    
    print("Searching for place coordinates...")
    places = []
    
    for place_name in places_to_visit:
        print(f"Finding: {place_name}")
        results = scraper.search_places_google(place_name)
        if results:
            places.extend(results)
            print(f"✓ Found: {results[0].name}")
        else:
            print(f"✗ Not found: {place_name}")
    
    print(f"\nFound {len(places)} places")
    
    # Create travel plan
    travel_plan = planner.create_travel_plan(places, max_places_per_day=3)
    
    print("\n=== TRAVEL PLAN ===")
    for day, day_places in travel_plan.items():
        print(f"\nDay {day}:")
        optimized_route = planner.optimize_route(day_places)
        
        for i, place in enumerate(optimized_route, 1):
            print(f"  {i}. {place.name}")
            print(f"     Coordinates: ({place.latitude:.4f}, {place.longitude:.4f})")
        
        # Show distances
        if len(optimized_route) > 1:
            total_distance = 0
            for i in range(len(optimized_route) - 1):
                distance_km = planner.calculate_distance(optimized_route[i], optimized_route[i + 1])
                total_distance += distance_km
                print(f"     → {optimized_route[i + 1].name}: {distance_km:.1f} km")
            print(f"     Total: {total_distance:.1f} km")

def example_custom_places():
    """Example with custom place data"""
    print("\n=== Custom Places Example ===\n")
    
    # Create places manually with known coordinates
    custom_places = [
        Place("Golden Gate Bridge", "San Francisco, CA", 37.8199, -122.4783),
        Place("Alcatraz Island", "San Francisco, CA", 37.8270, -122.4230),
        Place("Fisherman's Wharf", "San Francisco, CA", 37.8080, -122.4177),
        Place("Lombard Street", "San Francisco, CA", 37.8021, -122.4189),
        Place("Coit Tower", "San Francisco, CA", 37.8024, -122.4058),
        Place("Yosemite National Park", "California", 37.8651, -119.5383),  # Far away
    ]
    
    planner = TravelPlanner(max_distance_km=20.0)
    
    # Group nearby places
    groups = planner.group_nearby_places(custom_places)
    
    print("Place Groups (within 20km):")
    for i, group in enumerate(groups, 1):
        print(f"\nGroup {i}:")
        for place in group:
            print(f"  - {place.name}")
    
    # Create travel plan
    travel_plan = planner.create_travel_plan(custom_places, max_places_per_day=4)
    
    print(f"\n=== TRAVEL PLAN ===")
    for day, day_places in travel_plan.items():
        print(f"\nDay {day}:")
        for place in day_places:
            print(f"  - {place.name}")

def example_save_load():
    """Example of saving and loading place data"""
    print("\n=== Save/Load Example ===\n")
    
    scraper = PlaceScraper()
    
    # Search for some places
    place_names = ["Sagrada Familia, Barcelona", "Park Güell, Barcelona"]
    places = []
    
    for name in place_names:
        results = scraper.search_places_google(name)
        if results:
            places.extend(results)
    
    # Save to file
    data = []
    for place in places:
        place_data = {
            'name': place.name,
            'address': place.address,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'place_id': place.place_id,
            'rating': place.rating,
            'types': place.types
        }
        data.append(place_data)
    
    with open('example_places.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(places)} places to example_places.json")
    
    # Load from file
    with open('example_places.json', 'r') as f:
        loaded_data = json.load(f)
    
    loaded_places = []
    for place_data in loaded_data:
        place = Place(
            name=place_data['name'],
            address=place_data['address'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            place_id=place_data.get('place_id'),
            rating=place_data.get('rating'),
            types=place_data.get('types')
        )
        loaded_places.append(place)
    
    print(f"Loaded {len(loaded_places)} places from file")
    
    # Create plan with loaded places
    planner = TravelPlanner()
    travel_plan = planner.create_travel_plan(loaded_places)
    
    print("\nTravel plan from loaded data:")
    for day, day_places in travel_plan.items():
        print(f"Day {day}: {[p.name for p in day_places]}")

if __name__ == "__main__":
    # Run all examples
    example_basic_usage()
    example_custom_places()
    example_save_load()
    
    print("\n=== Examples Complete ===")
    print("Check 'example_places.json' for saved place data")
