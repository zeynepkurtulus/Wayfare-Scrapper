# Category Mapping Dictionary
# Maps current categories to standardized names with visit duration and type
# Reorganized for more logical grouping and realistic durations

CATEGORY_MAPPING = {
    # MAJOR ATTRACTIONS (2-4 hours) - Major museums, theme parks, large sites
    "Art Museums": {"new_category": "Major Museums", "duration": 180, "type": "major_attraction"},
    "History Museums": {"new_category": "Major Museums", "duration": 180, "type": "major_attraction"},
    "Science Museums": {"new_category": "Major Museums", "duration": 180, "type": "major_attraction"},
    "Natural History Museums": {"new_category": "Major Museums", "duration": 180, "type": "major_attraction"},
    "Children's Museums": {"new_category": "Major Museums", "duration": 150, "type": "major_attraction"},
    "Speciality Museums": {"new_category": "Major Museums", "duration": 150, "type": "major_attraction"},
    "Military Museums": {"new_category": "Major Museums", "duration": 150, "type": "major_attraction"},
    "Amusement & Theme Parks": {"new_category": "Theme Parks", "duration": 240, "type": "major_attraction"},
    "Disney Parks & Activities": {"new_category": "Theme Parks", "duration": 360, "type": "major_attraction"},
    "Water Parks": {"new_category": "Theme Parks", "duration": 240, "type": "major_attraction"},
    "National Parks": {"new_category": "Parks & Nature", "duration": 240, "type": "major_attraction"},
    "State Parks": {"new_category": "Parks & Nature", "duration": 180, "type": "major_attraction"},
    "Zoos": {"new_category": "Zoos & Aquariums", "duration": 180, "type": "major_attraction"},
    "Aquariums": {"new_category": "Zoos & Aquariums", "duration": 150, "type": "major_attraction"},
    "Islands": {"new_category": "Parks & Nature", "duration": 240, "type": "major_attraction"},
    "Mountains": {"new_category": "Parks & Nature", "duration": 240, "type": "major_attraction"},
    "Ski & Snowboard Areas": {"new_category": "Sports & Recreation", "duration": 240, "type": "major_attraction"},
    "Golf Courses": {"new_category": "Sports & Recreation", "duration": 240, "type": "major_attraction"},
    "Casinos": {"new_category": "Entertainment", "duration": 180, "type": "major_attraction"},
    "Spas": {"new_category": "Wellness & Relaxation", "duration": 180, "type": "major_attraction"},
    "Thermal Spas": {"new_category": "Wellness & Relaxation", "duration": 180, "type": "major_attraction"},
    "Onsen Resorts": {"new_category": "Wellness & Relaxation", "duration": 240, "type": "major_attraction"},
    
    # CULTURAL SITES (1-2 hours) - Historic sites, religious places, cultural venues
    "Historic Sites": {"new_category": "Cultural Sites", "duration": 120, "type": "cultural_site"},
    "Ancient Ruins": {"new_category": "Cultural Sites", "duration": 120, "type": "cultural_site"},
    "Castles": {"new_category": "Cultural Sites", "duration": 120, "type": "cultural_site"},
    "Churches & Cathedrals": {"new_category": "Religious Sites", "duration": 90, "type": "cultural_site"},
    "Religious Sites": {"new_category": "Religious Sites", "duration": 90, "type": "cultural_site"},
    "Missions": {"new_category": "Religious Sites", "duration": 90, "type": "cultural_site"},
    "Historic Walking Areas": {"new_category": "Cultural Sites", "duration": 120, "type": "cultural_site"},
    "Theaters": {"new_category": "Entertainment", "duration": 180, "type": "cultural_site"},
    "Operas": {"new_category": "Entertainment", "duration": 180, "type": "cultural_site"},
    "Concerts": {"new_category": "Entertainment", "duration": 180, "type": "cultural_site"},
    "Symphonies": {"new_category": "Entertainment", "duration": 180, "type": "cultural_site"},
    "Ballets": {"new_category": "Entertainment", "duration": 180, "type": "cultural_site"},
    "Art Galleries": {"new_category": "Cultural Sites", "duration": 90, "type": "cultural_site"},
    "Battlefields": {"new_category": "Cultural Sites", "duration": 90, "type": "cultural_site"},
    "Mines": {"new_category": "Cultural Sites", "duration": 90, "type": "cultural_site"},
    "Ghost Towns": {"new_category": "Cultural Sites", "duration": 90, "type": "cultural_site"},
    "Ships": {"new_category": "Cultural Sites", "duration": 90, "type": "cultural_site"},
    "Lighthouses": {"new_category": "Cultural Sites", "duration": 60, "type": "cultural_site"},
    "Cemeteries": {"new_category": "Cultural Sites", "duration": 60, "type": "cultural_site"},
    "Government Buildings": {"new_category": "Cultural Sites", "duration": 60, "type": "cultural_site"},
    "Libraries": {"new_category": "Cultural Sites", "duration": 60, "type": "cultural_site"},
    "Universities & Schools": {"new_category": "Cultural Sites", "duration": 60, "type": "cultural_site"},
    "Educational sites": {"new_category": "Cultural Sites", "duration": 60, "type": "cultural_site"},
    
    # OUTDOOR & NATURE (1-3 hours) - Parks, gardens, outdoor activities
    "Parks": {"new_category": "Parks & Nature", "duration": 120, "type": "outdoor_nature"},
    "Gardens": {"new_category": "Parks & Nature", "duration": 120, "type": "outdoor_nature"},
    "Beaches": {"new_category": "Parks & Nature", "duration": 180, "type": "outdoor_nature"},
    "Bodies of Water": {"new_category": "Parks & Nature", "duration": 60, "type": "outdoor_nature"},
    "Piers & Boardwalks": {"new_category": "Parks & Nature", "duration": 90, "type": "outdoor_nature"},
    "Marinas": {"new_category": "Parks & Nature", "duration": 60, "type": "outdoor_nature"},
    "Canyons": {"new_category": "Parks & Nature", "duration": 120, "type": "outdoor_nature"},
    "Caverns & Caves": {"new_category": "Parks & Nature", "duration": 90, "type": "outdoor_nature"},
    "Geologic Formations": {"new_category": "Parks & Nature", "duration": 60, "type": "outdoor_nature"},
    "Volcanos": {"new_category": "Parks & Nature", "duration": 120, "type": "outdoor_nature"},
    "Waterfalls": {"new_category": "Parks & Nature", "duration": 60, "type": "outdoor_nature"},
    "Valleys": {"new_category": "Parks & Nature", "duration": 90, "type": "outdoor_nature"},
    "Forests": {"new_category": "Parks & Nature", "duration": 120, "type": "outdoor_nature"},
    "Nature & Wildlife Areas": {"new_category": "Parks & Nature", "duration": 120, "type": "outdoor_nature"},
    "Reefs": {"new_category": "Parks & Nature", "duration": 120, "type": "outdoor_nature"},
    "Farms": {"new_category": "Parks & Nature", "duration": 90, "type": "outdoor_nature"},
    "Dams": {"new_category": "Parks & Nature", "duration": 60, "type": "outdoor_nature"},
    "Hot Springs & Geysers": {"new_category": "Parks & Nature", "duration": 90, "type": "outdoor_nature"},
    "Mysterious Sites": {"new_category": "Parks & Nature", "duration": 60, "type": "outdoor_nature"},
    "Lookouts": {"new_category": "Parks & Nature", "duration": 45, "type": "outdoor_nature"},
    "Observatories & Planetariums": {"new_category": "Parks & Nature", "duration": 90, "type": "outdoor_nature"},
    "Scenic Walking Areas": {"new_category": "Parks & Nature", "duration": 90, "type": "outdoor_nature"},
    "Scenic Drives": {"new_category": "Parks & Nature", "duration": 120, "type": "outdoor_nature"},
    "Scenic Railroads": {"new_category": "Parks & Nature", "duration": 120, "type": "outdoor_nature"},
    
    # SPORTS & RECREATION (1-3 hours) - Sports facilities, activities
    "Arenas & Stadiums": {"new_category": "Sports & Recreation", "duration": 180, "type": "sports_recreation"},
    "Auto Racing Tracks": {"new_category": "Sports & Recreation", "duration": 180, "type": "sports_recreation"},
    "Horse Tracks": {"new_category": "Sports & Recreation", "duration": 180, "type": "sports_recreation"},
    "Dog Tracks": {"new_category": "Sports & Recreation", "duration": 120, "type": "sports_recreation"},
    "Shooting Ranges": {"new_category": "Sports & Recreation", "duration": 90, "type": "sports_recreation"},
    "Sports Complexes": {"new_category": "Sports & Recreation", "duration": 120, "type": "sports_recreation"},
    "Health Clubs": {"new_category": "Sports & Recreation", "duration": 120, "type": "sports_recreation"},
    "Playgrounds": {"new_category": "Sports & Recreation", "duration": 60, "type": "sports_recreation"},
    "Miniature Golf": {"new_category": "Sports & Recreation", "duration": 90, "type": "sports_recreation"},
    "Biking Trails": {"new_category": "Sports & Recreation", "duration": 120, "type": "sports_recreation"},
    "Hiking Trails": {"new_category": "Sports & Recreation", "duration": 120, "type": "sports_recreation"},
    "Jogging Paths & Tracks": {"new_category": "Sports & Recreation", "duration": 60, "type": "sports_recreation"},
    "Equestrian Trails": {"new_category": "Sports & Recreation", "duration": 120, "type": "sports_recreation"},
    "Motorcycle Trails": {"new_category": "Sports & Recreation", "duration": 120, "type": "sports_recreation"},
    "Off-Road & ATV Trails": {"new_category": "Sports & Recreation", "duration": 180, "type": "sports_recreation"},
    
    # ENTERTAINMENT & NIGHTLIFE (1-3 hours) - Entertainment venues, nightlife
    "Bars & Clubs": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Breweries": {"new_category": "Entertainment", "duration": 90, "type": "entertainment"},
    "Distilleries": {"new_category": "Entertainment", "duration": 90, "type": "entertainment"},
    "Wineries & Vineyards": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Coffeehouses": {"new_category": "Entertainment", "duration": 60, "type": "entertainment"},
    "Wine Bars": {"new_category": "Entertainment", "duration": 90, "type": "entertainment"},
    "Jazz Bars": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Blues Bars": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Gay Bars": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Karaoke Bars": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Beach & Pool Clubs": {"new_category": "Entertainment", "duration": 180, "type": "entertainment"},
    "Dance Clubs & Discos": {"new_category": "Entertainment", "duration": 180, "type": "entertainment"},
    "Comedy Clubs": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Movie Theaters": {"new_category": "Entertainment", "duration": 180, "type": "entertainment"},
    "Dinner Theaters": {"new_category": "Entertainment", "duration": 240, "type": "entertainment"},
    "Cabarets": {"new_category": "Entertainment", "duration": 180, "type": "entertainment"},
    "Cirque du Soleil Shows": {"new_category": "Entertainment", "duration": 180, "type": "entertainment"},
    "Theater & Performances": {"new_category": "Entertainment", "duration": 180, "type": "entertainment"},
    "Cultural Events": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Exhibitions": {"new_category": "Entertainment", "duration": 90, "type": "entertainment"},
    "Music Festivals": {"new_category": "Entertainment", "duration": 240, "type": "entertainment"},
    "Sporting Events": {"new_category": "Entertainment", "duration": 180, "type": "entertainment"},
    "Game & Entertainment Centers": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Escape Games": {"new_category": "Entertainment", "duration": 60, "type": "entertainment"},
    "Scavenger Hunts": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Paint & Pottery Studios": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Hammams & Turkish Baths": {"new_category": "Wellness & Relaxation", "duration": 120, "type": "entertainment"},
    "Arab Baths": {"new_category": "Wellness & Relaxation", "duration": 120, "type": "entertainment"},
    "Roman Baths": {"new_category": "Wellness & Relaxation", "duration": 120, "type": "entertainment"},
    "Yoga & Pilates": {"new_category": "Wellness & Relaxation", "duration": 90, "type": "entertainment"},
    "Sports Camps & Clinics": {"new_category": "Sports & Recreation", "duration": 180, "type": "entertainment"},
    "Factory Tours": {"new_category": "Entertainment", "duration": 90, "type": "entertainment"},
    "Lessons & Workshops": {"new_category": "Entertainment", "duration": 120, "type": "entertainment"},
    "Cooking Classes": {"new_category": "Entertainment", "duration": 180, "type": "entertainment"},
    
    # SHOPPING & MARKETS (1-2 hours) - Shopping areas, markets
    "Shopping Malls": {"new_category": "Shopping & Markets", "duration": 120, "type": "shopping_markets"},
    "Department Stores": {"new_category": "Shopping & Markets", "duration": 90, "type": "shopping_markets"},
    "Flea & Street Markets": {"new_category": "Shopping & Markets", "duration": 90, "type": "shopping_markets"},
    "Farmers Markets": {"new_category": "Shopping & Markets", "duration": 60, "type": "shopping_markets"},
    "Factory Outlets": {"new_category": "Shopping & Markets", "duration": 120, "type": "shopping_markets"},
    "Antique Shops": {"new_category": "Shopping & Markets", "duration": 90, "type": "shopping_markets"},
    "Speciality & Gift Shops": {"new_category": "Shopping & Markets", "duration": 90, "type": "shopping_markets"},
    "Neighborhoods": {"new_category": "Shopping & Markets", "duration": 120, "type": "shopping_markets"},
    
    # TOURS & ACTIVITIES (2-4 hours) - Guided tours, activities
    "City Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Cultural Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Historical & Heritage Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Boat Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Food Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Shopping Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Sightseeing Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Walking Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Hop-On Hop-Off Tours": {"new_category": "Tours & Activities", "duration": 240, "type": "tours_activities"},
    "Private Tours": {"new_category": "Tours & Activities", "duration": 240, "type": "tours_activities"},
    "Night Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Photography Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Nature & Wildlife Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Eco Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Adrenaline & Extreme Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "4WD, ATV & Off-Road Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Bike Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Motorcycle Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Horseback Riding Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Balloon Rides": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Helicopter Tours": {"new_category": "Tours & Activities", "duration": 120, "type": "tours_activities"},
    "Air Tours": {"new_category": "Tours & Activities", "duration": 120, "type": "tours_activities"},
    "Skydiving": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Parasailing & Paragliding": {"new_category": "Tours & Activities", "duration": 120, "type": "tours_activities"},
    "Canyoning & Rappelling Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Zipline & Aerial Adventure Parks": {"new_category": "Tours & Activities", "duration": 120, "type": "tours_activities"},
    "Scuba & Snorkelling": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Shark Diving": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Swim with Dolphins": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Dolphin & Whale Watching": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Surfing & Windsurfing": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Waterskiing & Jetskiing": {"new_category": "Tours & Activities", "duration": 120, "type": "tours_activities"},
    "Stand Up Paddleboarding": {"new_category": "Tours & Activities", "duration": 120, "type": "tours_activities"},
    "Kayaking & Canoeing": {"new_category": "Tours & Activities", "duration": 120, "type": "tours_activities"},
    "River Rafting & Tubing": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Submarine Tours": {"new_category": "Tours & Activities", "duration": 120, "type": "tours_activities"},
    "Safaris": {"new_category": "Tours & Activities", "duration": 240, "type": "tours_activities"},
    "Hiking & Camping Tours": {"new_category": "Tours & Activities", "duration": 240, "type": "tours_activities"},
    "Multi-day Tours": {"new_category": "Tours & Activities", "duration": 1440, "type": "tours_activities"},
    "Day Trips": {"new_category": "Tours & Activities", "duration": 480, "type": "tours_activities"},
    "Wine Tours & Tastings": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Character Experiences": {"new_category": "Tours & Activities", "duration": 60, "type": "tours_activities"},
    "Seasonal Fireworks": {"new_category": "Tours & Activities", "duration": 60, "type": "tours_activities"},
    "Self-Guided Tours & Rentals": {"new_category": "Tours & Activities", "duration": 120, "type": "tours_activities"},
    "Bar, Club & Pub Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Speed Boats Tours": {"new_category": "Tours & Activities", "duration": 120, "type": "tours_activities"},
    "Bus Tours": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    "Rail Tours": {"new_category": "Tours & Activities", "duration": 240, "type": "tours_activities"},
    "Rides & Activities": {"new_category": "Tours & Activities", "duration": 180, "type": "tours_activities"},
    
    # QUICK VISITS (30-60 minutes) - Monuments, landmarks, quick stops
    "Monuments & Statues": {"new_category": "Landmarks & Monuments", "duration": 45, "type": "quick_visit"},
    "Fountains": {"new_category": "Landmarks & Monuments", "duration": 30, "type": "quick_visit"},
    "Bridges": {"new_category": "Landmarks & Monuments", "duration": 45, "type": "quick_visit"},
    "Points of Interest & Landmarks": {"new_category": "Landmarks & Monuments", "duration": 60, "type": "quick_visit"},
    "Observation Decks & Towers": {"new_category": "Landmarks & Monuments", "duration": 90, "type": "quick_visit"},
    "Wedding Chapels": {"new_category": "Landmarks & Monuments", "duration": 30, "type": "quick_visit"},
    "Visitor Centers": {"new_category": "Landmarks & Monuments", "duration": 30, "type": "quick_visit"},
    "Convention Centers": {"new_category": "Landmarks & Monuments", "duration": 60, "type": "quick_visit"},
    "Civic Centres": {"new_category": "Landmarks & Monuments", "duration": 60, "type": "quick_visit"},
    "Military Bases & Facilities": {"new_category": "Landmarks & Monuments", "duration": 60, "type": "quick_visit"},
    "Trams": {"new_category": "Transportation", "duration": 30, "type": "quick_visit"},
    "Public Transportation Systems": {"new_category": "Transportation", "duration": 30, "type": "quick_visit"},
    "Rail Services": {"new_category": "Transportation", "duration": 30, "type": "quick_visit"},
    "Ferries": {"new_category": "Transportation", "duration": 45, "type": "quick_visit"},
    "Bus Services": {"new_category": "Transportation", "duration": 30, "type": "quick_visit"},
    "Taxis & Shuttles": {"new_category": "Transportation", "duration": 30, "type": "quick_visit"},
    "Gear Rentals": {"new_category": "Transportation", "duration": 30, "type": "quick_visit"},
    
    # OTHER CATEGORIES
    "Other": {"new_category": "Other", "duration": 60, "type": "other"},
    "Other Food & Drink": {"new_category": "Other", "duration": 90, "type": "other"},
    "Food & Drink Festivals": {"new_category": "Entertainment", "duration": 180, "type": "other"},
    
    # Default fallback for unmapped categories
    "": {"new_category": "Other", "duration": 60, "type": "other"}
}

# Add mappings for combined categories (those with "•" separator)
def add_combined_category_mappings():
    """Add mappings for categories that contain multiple types separated by '•'"""
    combined_mappings = {}
    
    for category, mapping in CATEGORY_MAPPING.items():
        if "•" in category:
            # For combined categories, use the first category as primary
            primary_category = category.split("•")[0].strip()
            if primary_category in CATEGORY_MAPPING:
                combined_mappings[category] = CATEGORY_MAPPING[primary_category]
            else:
                # Default to medium visit for combined categories
                combined_mappings[category] = {"new_category": "Combined Attractions", "duration": 180, "type": "tours_activities"}
    
    CATEGORY_MAPPING.update(combined_mappings)

# Initialize combined mappings
add_combined_category_mappings()

# Function to get category mapping
def get_category_mapping(category_name):
    """Get the mapping for a given category name"""
    return CATEGORY_MAPPING.get(category_name, CATEGORY_MAPPING["Other"])

# Function to get all unique new categories
def get_all_new_categories():
    """Get all unique new category names"""
    return list(set(mapping["new_category"] for mapping in CATEGORY_MAPPING.values()))

# Function to get categories by duration type
def get_categories_by_type(visit_type):
    """Get all categories for a specific visit type"""
    return [mapping["new_category"] for mapping in CATEGORY_MAPPING.values() if mapping["type"] == visit_type]

# Function to get summary of new category structure
def get_category_summary():
    """Get a summary of the new category structure"""
    categories = {}
    for mapping in CATEGORY_MAPPING.values():
        cat_name = mapping["new_category"]
        if cat_name not in categories:
            categories[cat_name] = {
                "duration": mapping["duration"],
                "type": mapping["type"],
                "count": 0
            }
        categories[cat_name]["count"] += 1
    
    return categories
