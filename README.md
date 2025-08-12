# Places Scraper + Travel Planner

A Python project for scraping attraction data (prices, opening hours, categories) and generating travel plans by grouping nearby places.

## Repo structure

- `src/`: Main application and examples
  - `scrapper.py`, `travel_planner_app.py`, `example_usage.py`
- `cities/`, `raw_data/`, `updated_cities/`: JSON datasets and utilities
- `generative_files/`: One-off scripts for scraping, fixing URLs, and utilities
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
python src/travel_planner_app.py
```

Generate a sample plan programmatically:

```bash
python src/generate_paris_plan.py
```

## Development

- Python 3.10+
- Selenium flows may require Chrome installed; use `generative_files/setup_chromedriver.py` if needed.
- Data files live under `cities/`, `raw_data/`, `updated_cities/`.

## Contributing

Issues and PRs welcome. See docs and scripts for entry points.

## License

MIT — see `LICENSE`.
