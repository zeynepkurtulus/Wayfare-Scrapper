#!/usr/bin/env python3
"""
Interactive Travel Planner Application
Creates customized travel plans by grouping nearby places together
"""

import json
import os
from typing import List, Dict
from wayfare_scrapper import PlaceScraper, TravelPlanner, Place

class TravelPlannerApp:
    def __init__(self):
        self.scraper = PlaceScraper()
        self.planner = TravelPlanner()
        self.places = []
        
    def load_places_from_file(self, filename: str) -> bool:
        """Load places from a JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.places = []
                for place_data in data:
                    place = Place(
                        name=place_data['name'],
                        address=place_data['address'],
                        latitude=place_data['latitude'],
                        longitude=place_data['longitude'],
                        place_id=place_data.get('place_id'),
                        rating=place_data.get('rating'),
                        types=place_data.get('types')
                    )
                    self.places.append(place)
            print(f"Loaded {len(self.places)} places from {filename}")
            return True
        except FileNotFoundError:
            print(f"File {filename} not found")
            return False
        except json.JSONDecodeError:
            print(f"Invalid JSON in {filename}")
            return False
    
    def save_places_to_file(self, filename: str) -> bool:
        """Save places to a JSON file"""
        try:
            data = []
            for place in self.places:
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
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(self.places)} places to {filename}")
            return True
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return False
    
    def add_places_manually(self):
        """Add places manually by user input"""
        print("\n=== Add Places Manually ===")
        print("Enter place names (one per line). Press Enter twice to finish:")
        
        place_names = []
        while True:
            name = input("Place name: ").strip()
            if not name:
                break
            place_names.append(name)
        
        print(f"\nSearching for {len(place_names)} places...")
        
        for name in place_names:
            print(f"Searching for: {name}")
            results = self.scraper.search_places_google(name)
            if results:
                self.places.extend(results)
                print(f"✓ Found: {results[0].name}")
            else:
                print(f"✗ Could not find: {name}")
        
        print(f"\nTotal places: {len(self.places)}")
    
    def add_places_from_list(self):
        """Add places from a predefined list"""
        print("\n=== Predefined Place Lists ===")
        print("1. Paris Attractions")
        print("2. Rome Attractions")
        print("3. New York Attractions")
        print("4. London Attractions")
        print("5. Tokyo Attractions")
        
        choice = input("Select a list (1-5): ").strip()
        
        place_lists = {
            '1': [
                "Eiffel Tower, Paris",
                "Louvre Museum, Paris",
                "Notre-Dame Cathedral, Paris",
                "Arc de Triomphe, Paris",
                "Champs-Élysées, Paris",
                "Montmartre, Paris",
                "Sacre-Coeur, Paris",
                "Palace of Versailles, France"
            ],
            '2': [
                "Colosseum, Rome",
                "Vatican Museums, Vatican City",
                "St. Peter's Basilica, Vatican City",
                "Trevi Fountain, Rome",
                "Pantheon, Rome",
                "Roman Forum, Rome",
                "Piazza Navona, Rome",
                "Castel Sant'Angelo, Rome"
            ],
            '3': [
                "Statue of Liberty, New York",
                "Central Park, New York",
                "Times Square, New York",
                "Empire State Building, New York",
                "Brooklyn Bridge, New York",
                "Metropolitan Museum of Art, New York",
                "Broadway, New York",
                "Rockefeller Center, New York"
            ],
            '4': [
                "Big Ben, London",
                "Tower of London, London",
                "Buckingham Palace, London",
                "London Eye, London",
                "Tower Bridge, London",
                "British Museum, London",
                "Westminster Abbey, London",
                "Hyde Park, London"
            ],
            '5': [
                "Tokyo Tower, Tokyo",
                "Senso-ji Temple, Tokyo",
                "Shibuya Crossing, Tokyo",
                "Tokyo Skytree, Tokyo",
                "Meiji Shrine, Tokyo",
                "Tsukiji Fish Market, Tokyo",
                "Ueno Park, Tokyo",
                "Akihabara, Tokyo"
            ]
        }
        
        if choice in place_lists:
            places_to_add = place_lists[choice]
            print(f"\nSearching for {len(places_to_add)} places...")
            
            for place_name in places_to_add:
                print(f"Searching for: {place_name}")
                results = self.scraper.search_places_google(place_name)
                if results:
                    self.places.extend(results)
                    print(f"✓ Found: {results[0].name}")
                else:
                    print(f"✗ Could not find: {place_name}")
            
            print(f"\nTotal places: {len(self.places)}")
        else:
            print("Invalid choice")
    
    def create_travel_plan(self):
        """Create and display a travel plan"""
        if not self.places:
            print("No places added yet. Please add some places first.")
            return
        
        print("\n=== Travel Plan Settings ===")
        try:
            max_distance = float(input("Maximum distance between places (km) [30]: ") or "30")
            max_places_per_day = int(input("Maximum places per day [4]: ") or "4")
        except ValueError:
            print("Invalid input, using default values")
            max_distance = 30
            max_places_per_day = 4
        
        self.planner.max_distance_km = max_distance
        travel_plan = self.planner.create_travel_plan(self.places, max_places_per_day)
        
        print(f"\n=== TRAVEL PLAN ===")
        print(f"Total places: {len(self.places)}")
        print(f"Total days: {len(travel_plan)}")
        print(f"Max distance: {max_distance} km")
        print(f"Max places per day: {max_places_per_day}")
        
        for day, day_places in travel_plan.items():
            print(f"\n📅 Day {day} ({len(day_places)} places):")
            
            # Optimize route for this day
            optimized_route = self.planner.optimize_route(day_places)
            
            for i, place in enumerate(optimized_route, 1):
                print(f"  {i}. 📍 {place.name}")
                print(f"     📍 Coordinates: ({place.latitude:.4f}, {place.longitude:.4f})")
                if place.rating:
                    print(f"     ⭐ Rating: {place.rating}")
            
            # Show distances
            if len(optimized_route) > 1:
                print("  🚗 Distances:")
                total_distance = 0
                for i in range(len(optimized_route) - 1):
                    distance_km = self.planner.calculate_distance(optimized_route[i], optimized_route[i + 1])
                    total_distance += distance_km
                    print(f"     {optimized_route[i].name} → {optimized_route[i + 1].name}: {distance_km:.1f} km")
                print(f"     📊 Total distance for day: {total_distance:.1f} km")
    
    def show_places(self):
        """Display all current places"""
        if not self.places:
            print("No places added yet.")
            return
        
        print(f"\n=== Current Places ({len(self.places)}) ===")
        for i, place in enumerate(self.places, 1):
            print(f"{i}. {place.name}")
            print(f"   📍 {place.address}")
            print(f"   📍 ({place.latitude:.4f}, {place.longitude:.4f})")
            if place.rating:
                print(f"   ⭐ {place.rating}")
            print()
    
    def remove_place(self):
        """Remove a place from the list"""
        if not self.places:
            print("No places to remove.")
            return
        
        self.show_places()
        try:
            index = int(input("Enter the number of the place to remove: ")) - 1
            if 0 <= index < len(self.places):
                removed = self.places.pop(index)
                print(f"Removed: {removed.name}")
            else:
                print("Invalid index")
        except ValueError:
            print("Invalid input")
    
    def run(self):
        """Main application loop"""
        print("🌍 Welcome to the Travel Planner!")
        print("Create customized travel plans by grouping nearby places together.")
        
        while True:
            print("\n" + "="*50)
            print("📋 MAIN MENU")
            print("="*50)
            print("1. Add places manually")
            print("2. Add places from predefined list")
            print("3. Load places from file")
            print("4. Save places to file")
            print("5. Show current places")
            print("6. Remove a place")
            print("7. Create travel plan")
            print("8. Exit")
            
            choice = input("\nSelect an option (1-8): ").strip()
            
            if choice == '1':
                self.add_places_manually()
            elif choice == '2':
                self.add_places_from_list()
            elif choice == '3':
                filename = input("Enter filename: ").strip()
                self.load_places_from_file(filename)
            elif choice == '4':
                filename = input("Enter filename: ").strip()
                self.save_places_to_file(filename)
            elif choice == '5':
                self.show_places()
            elif choice == '6':
                self.remove_place()
            elif choice == '7':
                self.create_travel_plan()
            elif choice == '8':
                print("👋 Thanks for using the Travel Planner!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = TravelPlannerApp()
    app.run()
