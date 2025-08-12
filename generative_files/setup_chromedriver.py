#!/usr/bin/env python3
"""
Setup script for ChromeDriver
Automatically downloads and configures ChromeDriver for the scraping scripts
"""

import os
import sys
import subprocess
from webdriver_manager.chrome import ChromeDriverManager

def setup_chromedriver():
    """Setup ChromeDriver automatically"""
    try:
        print("Setting up ChromeDriver...")
        
        # Use webdriver-manager to automatically download and setup ChromeDriver
        driver_path = ChromeDriverManager().install()
        
        print(f"✓ ChromeDriver installed successfully at: {driver_path}")
        print("✓ You can now run the scraping scripts")
        
        return True
        
    except Exception as e:
        print(f"✗ Error setting up ChromeDriver: {e}")
        print("\nManual setup instructions:")
        print("1. Download ChromeDriver from: https://chromedriver.chromium.org/")
        print("2. Extract the executable to a directory in your PATH")
        print("3. Make sure you have Google Chrome installed")
        return False

def check_chrome_installation():
    """Check if Chrome is installed"""
    try:
        # Try to find Chrome in common locations
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",    # Windows
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe", # Windows
            "/usr/bin/google-chrome",  # Linux
            "/usr/bin/chromium-browser"  # Linux
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"✓ Chrome found at: {path}")
                return True
        
        # Try using 'which' command
        try:
            result = subprocess.run(['which', 'google-chrome'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Chrome found at: {result.stdout.strip()}")
                return True
        except:
            pass
        
        print("⚠️  Chrome not found in common locations")
        print("Please make sure Google Chrome is installed")
        return False
        
    except Exception as e:
        print(f"Error checking Chrome installation: {e}")
        return False

def main():
    print("ChromeDriver Setup Script")
    print("=" * 30)
    
    # Check if Chrome is installed
    if not check_chrome_installation():
        print("\nPlease install Google Chrome first:")
        print("https://www.google.com/chrome/")
        return
    
    # Setup ChromeDriver
    if setup_chromedriver():
        print("\n✓ Setup completed successfully!")
        print("You can now run: python scrape_duration_from_tripadvisor.py")
    else:
        print("\n✗ Setup failed. Please follow the manual instructions above.")

if __name__ == "__main__":
    main() 