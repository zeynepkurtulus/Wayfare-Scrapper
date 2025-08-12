
# URL FIXING INSTRUCTIONS

## Problem
Most of the detail_url fields in your JSON files are incorrect - they point to different attractions than the name suggests.

## Solution Options

### Option 1: Manual Fixing (Recommended)
1. Run the script to create a mapping file:
   python generative_files/fix_urls_comprehensive_search.py

2. Edit the generated `url_mapping_for_manual_fix.json` file:
   - Find entries where "needs_fix": true
   - Add a "corrected_url" field with the correct TripAdvisor URL
   - You can find correct URLs by:
     * Going to TripAdvisor.com
     * Searching for "{attraction_name} {city_name}"
     * Copying the URL from the attraction page

3. Apply the fixes:
   python generative_files/apply_url_fixes.py

### Option 2: Automated Search (Advanced)
For a fully automated solution, you would need to:
1. Use Google Search API or similar
2. Search for "{attraction_name} {city_name} site:tripadvisor.com"
3. Parse results to find correct URLs
4. Verify URLs are actually correct

### Option 3: Skip URL Fixing
If you don't need the duration scraping feature, you can skip this step entirely.

## Current Status
- Total entries: ~11,130
- Incorrect URLs: ~10,796 (97%)
- Correct URLs: ~334 (3%)

## Next Steps
1. Decide which approach to take
2. If manual fixing: Start with a few cities to test the process
3. If automated: Implement proper search functionality
4. If skipping: Proceed with other data enrichment tasks
