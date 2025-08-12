#!/usr/bin/env python3
"""
Backup Script for Category Mapping
Creates a backup of all JSON files before applying category mapping
"""

import os
import json
import shutil
from datetime import datetime

def create_backup():
    """Create a backup of all JSON files in the cities directory"""
    cities_dir = 'cities'
    backup_dir = f'backup_categories_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    print("Category Mapping Backup Script")
    print("=" * 40)
    print(f"Creating backup in: {backup_dir}")
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    backup_count = 0
    total_size = 0
    
    for filename in os.listdir(cities_dir):
        if filename.endswith('_attractions_with_hours_and_price.json'):
            source_path = os.path.join(cities_dir, filename)
            backup_path = os.path.join(backup_dir, filename)
            
            try:
                # Copy the file
                shutil.copy2(source_path, backup_path)
                file_size = os.path.getsize(backup_path)
                total_size += file_size
                backup_count += 1
                print(f"  ✓ Backed up: {filename} ({file_size:,} bytes)")
            except Exception as e:
                print(f"  ✗ Failed to backup {filename}: {e}")
    
    print(f"\n✅ Backup completed!")
    print(f"Files backed up: {backup_count}")
    print(f"Total size: {total_size:,} bytes")
    print(f"Backup location: {backup_dir}")
    
    return backup_dir

def main():
    try:
        response = input("Create backup before applying category mapping? (Y/n): ").strip().lower()
        if response in ['n', 'no']:
            print("Skipping backup. Proceed with caution!")
            return
        
        backup_dir = create_backup()
        print(f"\nYou can now safely run: python apply_category_mapping.py")
        print(f"If something goes wrong, restore from: {backup_dir}")
        
    except KeyboardInterrupt:
        print("\nBackup cancelled.")
        return

if __name__ == "__main__":
    main() 