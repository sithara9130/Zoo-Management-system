"""
Main Launcher for Zoo Management System
Save as: main.py

This is the file you run to start the application!
Just run: python main.py
"""

from common import *

def main():
    """Start the Zoo Management System"""
    print("=" * 60)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print("Starting application...")
    print("Opening login window...")
    
    # Open login window
    NavigationManager.open_login()

if __name__ == "__main__":
    main()
