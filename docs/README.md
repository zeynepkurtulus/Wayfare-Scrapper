#Travel Planner Application

A Python application that creates customized travel plans by grouping nearby places together. The app scrapes place coordinates and intelligently organizes them into daily itineraries based on proximity.

## Features

- **Place Coordinate Scraping**: Automatically finds coordinates for places using Google Places API or free geocoding services
- **Smart Grouping**: Groups nearby places together based on configurable distance thresholds
- **Route Optimization**: Optimizes the order of visits within each day using nearest neighbor algorithm
- **Interactive Interface**: User-friendly command-line interface with multiple input options
- **Data Persistence**: Save and load place data in JSON format
- **Predefined Lists**: Quick access to popular attractions in major cities

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the interactive application:

```bash
python travel_planner_app.py
```

### Basic Usage

1. **Add Places**: Choose from predefined lists or add places manually
2. **Configure Settings**: Set maximum distance between places and places per day
3. **Generate Plan**: Create an optimized travel plan
4. **Save/Load**: Save your places for future use

### Example Workflow

```
1. Start the application
2. Choose "Add places from predefined list"
3. Select "Paris Attractions"
4. Choose "Create travel plan"
5. Set max distance to 30 km and max places per day to 4
6. View your optimized travel plan!
```

## Files

- `scrapper.py`: Core scraping and planning logic
- `travel_planner_app.py`: Interactive user interface
- `requirements.txt`: Python dependencies
- `README.md`: This documentation

## API Keys (Optional)

For enhanced functionality, you can add a Google Places API key:

1. Get a Google Places API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Modify the `PlaceScraper` initialization in the code:

```python
scraper = PlaceScraper(google_api_key="YOUR_API_KEY_HERE")
```

**Note**: The application works without an API key using free geocoding services, but with limited functionality.

## How It Works

### 1. Place Scraping
- Uses Google Places API (if available) or Nominatim geocoding service
- Extracts coordinates, ratings, and other place information
- Handles errors gracefully with fallback methods

### 2. Distance Calculation
- Uses geodesic distance calculation for accurate results
- Considers Earth's curvature for precise measurements

### 3. Place Grouping
- Groups places within a specified maximum distance
- Sorts places geographically for efficient clustering
- Prevents overlapping groups

### 4. Route Optimization
- Uses nearest neighbor algorithm for each day's route
- Minimizes total travel distance within each group
- Provides distance information between consecutive places

## Example Output

```
=== TRAVEL PLAN ===
Total places: 8
Total days: 2
Max distance: 30 km
Max places per day: 4

 Day 1 (4 places):
  1.  Eiffel Tower
      Coordinates: (48.8584, 2.2945)
      Rating: 4.6
  2.  Arc de Triomphe
      Coordinates: (48.8738, 2.2950)
      Rating: 4.4
  3.  Champs-Élysées
      Coordinates: (48.8698, 2.3077)
  4. Louvre Museum
     Coordinates: (48.8606, 2.3376)
     Rating: 4.7
   Distances:
     Eiffel Tower → Arc de Triomphe: 1.7 km
     Arc de Triomphe → Champs-Élysées: 0.9 km
     Champs-Élysées → Louvre Museum: 2.5 km
      Total distance for day: 5.1 km
```

## Customization

### Adjusting Distance Thresholds
Modify the `max_distance_km` parameter in the `TravelPlanner` class:

```python
planner = TravelPlanner(max_distance_km=50.0)  # 50 km instead of default 30 km
```

### Adding New Place Lists
Extend the `place_lists` dictionary in `travel_planner_app.py`:

```python
'6': [
    "Your Custom Place 1",
    "Your Custom Place 2",
    # ... more places
]
```

### Custom Place Data Format
When saving/loading places, the JSON format is:

```json
[
  {
    "name": "Place Name",
    "address": "Full Address",
    "latitude": 48.8584,
    "longitude": 2.2945,
    "place_id": "optional_google_place_id",
    "rating": 4.6,
    "types": ["tourist_attraction", "point_of_interest"]
  }
]
```

## Troubleshooting

### Common Issues

1. **"Could not find coordinates"**: 
   - Try more specific place names
   - Add city/country to the place name
   - Check internet connection

2. **API Rate Limits**:
   - The app includes delays between requests
   - Consider using a Google Places API key for better reliability

3. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

### Performance Tips

- Use specific place names for better geocoding results
- Save your place lists to avoid re-scraping
- Adjust distance thresholds based on your travel style

## Contributing

Feel free to contribute improvements:
- Add new place lists
- Implement additional optimization algorithms
- Enhance the user interface
- Add new data sources

## License

This project is open source and available under the MIT License. 
