# Places Scraper + Travel Planner

A Python project for scraping attraction data (prices, opening hours, categories) and generating travel plans by grouping nearby places.

## Repo structure

- `wayfare_scrapper/`: Python package with core logic (`Place`, `PlaceScraper`, `TravelPlanner`) and data utilities
  - `core.py`
  - `data/category_mapping.py`
- `scripts/`: Executable scripts and CLIs
  - `travel_planner_app.py`
  - `generate_paris_plan.py`
  - `apply_category_mapping.py`
  - `scrape_opening_hours.py`
  - `fix_urls_comprehensive_scraping.py`
- `examples/`: Example usage scripts
  - `example_usage.py`
- `cities/`, `raw_data/`, `updated_cities/`: JSON datasets and outputs
- `generative_files/`: Legacy/one-off scripts (now mostly migrated; remaining items may be removed later)
- `docs/`: Detailed documentation
- `diagrams/`: Architecture diagram
- `requirements.txt`: Dependencies

See `docs/README.md` and `docs/CODE_EXPLANATION.md` for deeper details.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # on macOS/Linux
pip install -r requirements.txt
```

Run the interactive app:

```bash
python scripts/travel_planner_app.py
```

Generate a sample plan programmatically:

```bash
python scripts/generate_paris_plan.py
```

Run examples:

```bash
python examples/example_usage.py
```

Run data utilities:

```bash
# Apply standardized category mapping and durations to city JSONs
python scripts/apply_category_mapping.py

# Scrape opening hours into existing *_with_hours_and_price.json files
python scripts/scrape_opening_hours.py

# Attempt to fix incorrect TripAdvisor detail URLs by scraping city index pages
python scripts/fix_urls_comprehensive_scraping.py
```

## Data (ignored in git)

The following directories are ignored by git to keep the repository slim:
- `cities/`
- `raw_data/`
- `updated_cities/`

If you need the datasets:
- Place your JSON files into these directories with the expected filenames, or
- Regenerate/update fields using the scripts above.

## Development

- Python 3.10+
- Selenium flows may require Chrome installed; run `python generative_files/setup_chromedriver.py` if needed.
- Data files live under `cities/`, `raw_data/`, `updated_cities/`.

## Contributing

Issues and PRs welcome. See docs and scripts for entry points.

