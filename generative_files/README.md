# Generative Files - Data Processing Pipeline

This directory contains scripts for processing, enriching, and fixing the places dataset. These scripts form a complete data pipeline that transforms raw attraction data into a structured, enriched format suitable for travel planning applications.

## 📁 File Overview

### 🔧 Data Enrichment Scripts

#### `add_popularity_from_raw.py` For adding pop field into attractions
**Purpose**: Extracts popularity rankings from numbered attraction names and adds them to the dataset.
- Reads `raw_data/` files containing numbered attractions (e.g., "1. Eiffel Tower")
- Extracts the ranking number and adds it as a `popularity` field
- Updates corresponding entries in `cities/` files
- **Output**: Adds `popularity` field (string) to each attraction

#### `add_country_to_attractions.py` For adding country fields into attractions
**Purpose**: Adds country information to each attraction.
- Maps city names to their respective countries
- Adds `country` and `country_id` fields to each attraction
- Uses predefined city-to-country mappings
- **Output**: Adds `country` and `country_id` fields to each attraction

#### `generate_city_ids.py` For adding city_id fields into attractions 
**Purpose**: Links attractions to city metadata.
- Adds `city_id` field to attractions by linking to `cities.json`
- Creates relationships between attractions and city metadata
- **Output**: Adds `city_id` field to each attraction

### 📊 Metadata Generation Scripts

#### `generate_cities_json.py` For db collection
**Purpose**: Creates a comprehensive cities metadata file. For generting the data to load to the cities collection in the database 
- Generates unique IDs for each city
- Creates structured city metadata with country information
- **Output**: `cities.json` file with city metadata

#### `generate_countries_json.py`  For db collection
**Purpose**: Creates a countries metadata file. For generting the data to load to the countries collection in the database 
- Defines country information with regions
- Creates structured country metadata
- **Output**: `countries.json` file with country metadata

### 🔍 Data Analysis & Validation Scripts

#### `scan_categories.py` For scanning types of cats in attractions
**Purpose**: Analyzes existing category data.
- Scans all JSON files to extract unique category values
- Helps understand current category structure
- **Output**: List of all unique categories found

#### `check_popularity_field.py`
**Purpose**: Validates data completeness.
- Checks if all attractions have the `popularity` field
- Reports missing fields by file and entry
- **Output**: Validation report of missing popularity fields

#### `validate_detail_urls.py`
**Purpose**: Validates URL correctness.
- Checks if `detail_url` fields match attraction names
- Identifies incorrect URLs by comparing normalized text
- **Output**: Report of URL mismatches and validation summary

### 🏷️ Category Management

#### `category_mapping.py` For reorganizing the categories 
**Purpose**: Standardizes and reorganizes categories.
- Defines mapping from raw categories to standardized ones
- Creates duration-based category system
- Provides readable category names
- **Output**: Comprehensive category mapping system

### 🌐 Web Scraping Scripts

#### `gpt.py`
**Purpose**: Core TripAdvisor scraping functionality.
- Extracts detailed attraction URLs from TripAdvisor city pages
- Handles pagination to get all attractions
- **Output**: List of attraction URLs for a given city

#### `fix_urls_comprehensive_scraping.py`
**Purpose**: Fixes incorrect URLs by scraping correct ones.
- Scrapes multiple pages of TripAdvisor attraction listings
- Updates incorrect `detail_url` fields with correct URLs
- Handles pagination and rate limiting
- **Output**: Updated JSON files with correct URLs

#### `scrape_duration_from_tripadvisor.py` For updating the duration field of attractions
**Purpose**: Extracts duration information from TripAdvisor using Chrome driver.
- Scrapes duration data from attraction detail pages using Selenium
- Handles JavaScript-rendered content more reliably
- Converts duration text to minutes
- Adds duration field to each attraction
- **Output**: Adds `duration` field (in minutes) to each attraction
- **Requirements**: Chrome browser and ChromeDriver (see setup instructions below)

## 🚀 Usage Workflow

### 📋 Logical Execution Order

The scripts should be executed in the following logical order to ensure data dependencies are met:

#### **Phase 1: Data Foundation** (Run First)
```bash
# 1. Add country information to attractions
python add_country_to_attractions.py

# 2. Generate metadata files (depends on country data)
python generate_cities_json.py
python generate_countries_json.py

# 3. Add city IDs (depends on cities.json)
python generate_city_ids.py
```

#### **Phase 2: Data Enrichment** (Run Second)
```bash
# 4. Add popularity rankings from raw data
python add_popularity_from_raw.py

# 5. Validate that popularity fields were added correctly
python check_popularity_field.py
```

#### **Phase 3: Data Analysis** (Run Third)
```bash
# 6. Analyze existing categories
python scan_categories.py

# 7. Validate URL correctness
python validate_detail_urls.py
```

#### **Phase 4: Data Fixing** (Run Fourth)
```bash
# 8. Fix incorrect URLs by scraping correct ones
python fix_urls_comprehensive_scraping.py
```

#### **Phase 5: Additional Data Collection** (Run Last)
```bash
# 9. Scrape duration information (depends on correct URLs)
python scrape_duration_from_tripadvisor.py
```

### 🔄 **Dependency Flow:**

```
Phase 1: Foundation
├── add_country_to_attractions.py
├── generate_cities_json.py (depends on country data)
├── generate_countries_json.py
└── generate_city_ids.py (depends on cities.json)

Phase 2: Enrichment
├── add_popularity_from_raw.py
└── check_popularity_field.py (validates Phase 2)

Phase 3: Analysis
├── scan_categories.py
└── validate_detail_urls.py

Phase 4: Fixing
└── fix_urls_comprehensive_scraping.py (depends on Phase 3 analysis)

Phase 5: Collection
└── scrape_duration_from_tripadvisor.py (depends on Phase 4 URL fixes)
```

### ⚠️ **Important Notes:**

- **Don't skip phases** - Each phase builds on the previous one
- **Run validation scripts** after each phase to ensure data quality
- **Backup your data** before running scripts that modify files
- **Check for errors** after each script execution
- **URL fixing is optional** - Only run if you need correct URLs for duration scraping

## 📋 Data Fields

### Original Fields (before processing)
- `name` - Attraction name
- `category` - Attraction category
- `price` - Price information
- `rating` - Rating value
- `image` - Image URL
- `detail_url` - TripAdvisor detail URL
- `opening_hours` - Opening hours data

### Added Fields (after processing)
- `_id` - MongoDB-style unique identifier
- `place_id` - UUID for the place
- `city` - City name
- `country` - Country name
- `country_id` - Country code
- `city_id` - City identifier
- `popularity` - Popularity ranking
- `coordinates` - Latitude/longitude
- `address` - Full address
- `source` - Data source (tripadvisor)
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp
- `duration` - Visit duration in minutes

## 🔧 Dependencies

- `requests` - HTTP requests for web scraping
- `beautifulsoup4` - HTML parsing
- `selenium` - Browser automation for JavaScript-heavy sites
- `webdriver-manager` - Automatic ChromeDriver management
- `geopy` - Geocoding functionality
- `uuid` - Unique ID generation
- `json` - JSON file handling
- `os` - File system operations
- `re` - Regular expressions
- `time` - Rate limiting and delays
- `random` - Random delays for scraping

## 🚀 Chrome Driver Setup

For scripts that use Selenium (like `scrape_duration_from_tripadvisor.py`), you need Chrome and ChromeDriver:

### Automatic Setup (Recommended)
```bash
# Run the setup script to automatically download and configure ChromeDriver
python setup_chromedriver.py
```

### Manual Setup
1. **Install Google Chrome** if not already installed
2. **Download ChromeDriver** from: https://chromedriver.chromium.org/
3. **Extract ChromeDriver** to a directory in your PATH
4. **Verify installation** by running: `chromedriver --version`

## 📝 Notes

- All scripts include rate limiting to be respectful to external services
- Error handling is implemented for network requests and file operations
- Scripts are designed to be run independently or as part of a pipeline
- Output files are saved in the appropriate directories (`cities/`, root directory)
- Validation scripts provide detailed reports for data quality assessment

## 🎯 Purpose

This collection of scripts transforms raw attraction data into a comprehensive, structured dataset suitable for:
- Travel planning applications
- Location-based services
- Data analysis and visualization
- API development
- Database population

The processed data includes all necessary information for building travel planning features like route optimization, duration estimation, and attraction recommendations. 