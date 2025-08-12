#!/usr/bin/env python3
"""
Apply Category Mapping Script
Adds wayfare_category and duration fields to JSON files based on category mapping
"""

import os
import json
import re
from category_mapping import get_category_mapping, get_category_summary, CATEGORY_MAPPING

def find_best_category_match(original_category):
    """Find the best matching category from the mapping, handling partial matches"""
    if not original_category:
        return None
    
    original_lower = original_category.lower().strip()
    
    # First try exact match
    if original_category in CATEGORY_MAPPING:
        return CATEGORY_MAPPING[original_category]
    
    # Try partial matches
    for mapping_key, mapping_value in CATEGORY_MAPPING.items():
        mapping_lower = mapping_key.lower()
        
        # Check if the original category contains key words from the mapping
        if any(word in original_lower for word in mapping_lower.split() if len(word) > 3):
            return mapping_value
        
        # Check if mapping key contains words from original category
        if any(word in mapping_lower for word in original_lower.split() if len(word) > 3):
            return mapping_value
    
    # Try fuzzy matching for common variations
    fuzzy_matches = {
        'museum': 'Major Museums',
        'park': 'Parks & Nature', 
        'garden': 'Parks & Nature',
        'beach': 'Parks & Nature',
        'castle': 'Cultural Sites',
        'church': 'Religious Sites',
        'cathedral': 'Religious Sites',
        'temple': 'Religious Sites',
        'mosque': 'Religious Sites',
        'synagogue': 'Religious Sites',
        'zoo': 'Zoos & Aquariums',
        'aquarium': 'Zoos & Aquariums',
        'theater': 'Entertainment',
        'theatre': 'Entertainment',
        'bar': 'Entertainment',
        'club': 'Entertainment',
        'restaurant': 'Entertainment',
        'cafe': 'Entertainment',
        'shopping': 'Shopping & Markets',
        'market': 'Shopping & Markets',
        'mall': 'Shopping & Markets',
        'sport': 'Sports & Recreation',
        'gym': 'Sports & Recreation',
        'fitness': 'Sports & Recreation',
        'tour': 'Tours & Activities',
        'activity': 'Tours & Activities',
        'spa': 'Wellness & Relaxation',
        'bath': 'Wellness & Relaxation',
        'monument': 'Landmarks & Monuments',
        'statue': 'Landmarks & Monuments',
        'fountain': 'Landmarks & Monuments',
        'bridge': 'Landmarks & Monuments',
        'tower': 'Landmarks & Monuments',
        'landmark': 'Landmarks & Monuments',
        'transport': 'Transportation',
        'bus': 'Transportation',
        'train': 'Transportation',
        'metro': 'Transportation',
        'subway': 'Transportation'
    }
    
    for keyword, category in fuzzy_matches.items():
        if keyword in original_lower:
            # Find the mapping for this category
            for mapping_key, mapping_value in CATEGORY_MAPPING.items():
                if mapping_value['new_category'] == category:
                    return mapping_value
    
    # Default fallback
    return CATEGORY_MAPPING.get("Other", {"new_category": "Other", "duration": 60, "type": "other"})

def apply_category_mapping_to_file(file_path):
    """Apply category mapping to a single JSON file, adding new fields"""
    try:
        # Load the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated_count = 0
        skipped_count = 0
        original_categories = set()
        new_categories = set()
        unmatched_categories = set()
        
        # Process each entry
        for entry in data:
            original_category = entry.get('category', '')
            if original_category:
                original_categories.add(original_category)
                
                # Check if fields already exist
                if 'wayfare_category' in entry and 'duration' in entry:
                    skipped_count += 1
                    continue
                
                # Find the best matching category
                mapping = find_best_category_match(original_category)
                
                if mapping:
                    # Add new fields
                    entry['wayfare_category'] = mapping['new_category']
                    entry['duration'] = mapping['duration']
                    
                    new_categories.add(mapping['new_category'])
                    updated_count += 1
                else:
                    # Use default for unmatched categories
                    default_mapping = CATEGORY_MAPPING.get("Other", {"new_category": "Other", "duration": 60, "type": "other"})
                    entry['wayfare_category'] = default_mapping['new_category']
                    entry['duration'] = default_mapping['duration']
                    unmatched_categories.add(original_category)
                    updated_count += 1
        
        # Save the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return {
            'filename': os.path.basename(file_path),
            'updated_count': updated_count,
            'skipped_count': skipped_count,
            'original_categories': len(original_categories),
            'new_categories': len(new_categories),
            'original_categories_list': list(original_categories),
            'new_categories_list': list(new_categories),
            'unmatched_categories': list(unmatched_categories)
        }
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    cities_dir = 'cities'
    
    print("Category Mapping Application Script")
    print("=" * 50)
    print("This script will ADD new fields to your JSON files:")
    print("  • wayfare_category: New standardized category")
    print("  • duration: Visit duration in minutes")
    print("  • Original 'category' field will be preserved")
    
    # Show the new category structure
    print("\n📋 New Category Structure:")
    summary = get_category_summary()
    for category, info in summary.items():
        print(f"  • {category}: {info['duration']} min ({info['type']}) - {info['count']} original categories")
    
    # Confirm with user
    print(f"\nThis will update all JSON files in the '{cities_dir}' directory.")
    try:
        response = input("Continue? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Operation cancelled.")
            return
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return
    
    # Process all JSON files
    results = []
    total_files = 0
    total_updated = 0
    total_skipped = 0
    all_unmatched = set()
    
    for filename in os.listdir(cities_dir):
        if filename.endswith('_attractions_with_hours_and_price.json'):
            file_path = os.path.join(cities_dir, filename)
            total_files += 1
            
            print(f"\nProcessing {filename}...")
            result = apply_category_mapping_to_file(file_path)
            
            if result:
                results.append(result)
                total_updated += result['updated_count']
                total_skipped += result['skipped_count']
                all_unmatched.update(result['unmatched_categories'])
                print(f"  ✓ Updated {result['updated_count']} entries")
                if result['skipped_count'] > 0:
                    print(f"  ⏭️  Skipped {result['skipped_count']} entries (already have fields)")
                print(f"  ✓ Original categories: {result['original_categories']} → New categories: {result['new_categories']}")
                if result['unmatched_categories']:
                    print(f"  ⚠️  Unmatched categories: {len(result['unmatched_categories'])}")
            else:
                print(f"  ✗ Failed to process {filename}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    print(f"Total files processed: {total_files}")
    print(f"Total entries updated: {total_updated}")
    print(f"Total entries skipped: {total_skipped}")
    
    # Show category transformation examples
    print("\n🔄 Category Transformation Examples:")
    for result in results[:3]:  # Show first 3 files as examples
        print(f"\n{result['filename']}:")
        for orig_cat in result['original_categories_list'][:5]:  # Show first 5 categories
            mapping = find_best_category_match(orig_cat)
            if mapping:
                print(f"  • {orig_cat} → {mapping['new_category']} ({mapping['duration']} min)")
            else:
                print(f"  • {orig_cat} → Other (60 min) [unmatched]")
        if len(result['original_categories_list']) > 5:
            print(f"  ... and {len(result['original_categories_list']) - 5} more categories")
    
    # Show unmatched categories
    if all_unmatched:
        print(f"\n⚠️  Unmatched Categories ({len(all_unmatched)}):")
        for unmatched in sorted(all_unmatched)[:10]:  # Show first 10
            print(f"  • {unmatched}")
        if len(all_unmatched) > 10:
            print(f"  ... and {len(all_unmatched) - 10} more")
    
    print(f"\n✅ Category mapping applied successfully!")
    print("New fields 'wayfare_category' and 'duration' have been added to all JSON files.")
    print("Original 'category' fields have been preserved.")

if __name__ == "__main__":
    main() 