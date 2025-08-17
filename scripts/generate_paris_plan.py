#!/usr/bin/env python3
"""
Generate a 4-day Paris travel plan and save to paris_plan.json
"""

import json
from wayfare_scrapper import PlaceScraper, TravelPlanner, Place

def generate_paris_plan():
    """Generate a comprehensive 4-day Paris travel plan"""
    
    # Initialize scraper and planner
    scraper = PlaceScraper()
    planner = TravelPlanner(max_distance_km=25.0)  # 25km max distance between places
    
    # Comprehensive list of Paris attractions
    paris_attractions = [
        "Eiffel Tower, Paris",
        "Louvre Museum, Paris",
        "Notre-Dame Cathedral, Paris",
        "Arc de Triomphe, Paris",
        "Champs-Élysées, Paris",
        "Montmartre, Paris",
        "Sacre-Coeur, Paris",
        "Palace of Versailles, France",
        "Musée d'Orsay, Paris",
        "Centre Pompidou, Paris",
        "Luxembourg Gardens, Paris",
        "Panthéon, Paris",
        "Sainte-Chapelle, Paris",
        "Place de la Concorde, Paris",
        "Tuileries Garden, Paris",
        "Palais Garnier, Paris",
        "Disneyland Paris, France",
        "Château de Fontainebleau, France"
    ]
    
    print("🌍 Generating Paris Travel Plan...")
    print(f"Searching for {len(paris_attractions)} attractions...")
    
    # Find coordinates for all places
    places = []
    for i, attraction in enumerate(paris_attractions, 1):
        print(f"[{i}/{len(paris_attractions)}] Finding: {attraction}")
        results = scraper.search_places_google(attraction)
        if results:
            places.extend(results)
            print(f"  ✓ Found: {results[0].name}")
        else:
            print(f"  ✗ Could not find: {attraction}")
    
    print(f"\n✅ Found coordinates for {len(places)} places")
    
    # Create travel plan for 4 days
    travel_plan = planner.create_travel_plan(places, max_places_per_day=5)
    
    # Prepare data for JSON output
    plan_data = {
        "city": "Paris",
        "total_places": len(places),
        "total_days": len(travel_plan),
        "max_distance_km": 25.0,
        "max_places_per_day": 5,
        "days": {}
    }
    
    # Process each day
    for day_num, day_places in travel_plan.items():
        # Optimize route for this day
        optimized_route = planner.optimize_route(day_places)
        
        day_data = {
            "day_number": day_num,
            "total_places": len(optimized_route),
            "total_distance_km": 0,
            "places": []
        }
        
        # Calculate distances and prepare place data
        for i, place in enumerate(optimized_route):
            place_data = {
                "order": i + 1,
                "name": place.name,
                "address": place.address,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "rating": place.rating,
                "distance_from_previous": 0
            }
            
            # Calculate distance from previous place
            if i > 0:
                distance_km = planner.calculate_distance(optimized_route[i-1], place)
                place_data["distance_from_previous"] = round(distance_km, 1)
                day_data["total_distance_km"] += distance_km
            
            day_data["places"].append(place_data)
        
        day_data["total_distance_km"] = round(day_data["total_distance_km"], 1)
        plan_data["days"][day_num] = day_data
    
    # Save to JSON file
    with open('paris_plan.json', 'w', encoding='utf-8') as f:
        json.dump(plan_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Travel plan saved to 'paris_plan.json'")
    
    # Display summary
    print(f"\n🗺️ PARIS TRAVEL PLAN SUMMARY")
    print(f"Total places: {len(places)}")
    print(f"Total days: {len(travel_plan)}")
    print(f"Max distance between places: 25 km")
    print(f"Max places per day: 5")
    
    for day_num, day_places in travel_plan.items():
        optimized_route = planner.optimize_route(day_places)
        total_distance = 0
        for i in range(len(optimized_route) - 1):
            total_distance += planner.calculate_distance(optimized_route[i], optimized_route[i + 1])
        
        print(f"\n📅 Day {day_num} ({len(optimized_route)} places, {total_distance:.1f} km):")
        for i, place in enumerate(optimized_route, 1):
            print(f"  {i}. {place.name}")
    
    return plan_data

if __name__ == "__main__":
    generate_paris_plan()
