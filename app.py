"""
POS System Application

Author: Alejandro Vargas
Github: https://github.com/sagravela

This script serves as the entry point for the POS System Application. It initializes 
the application, sets up the database, loads the stylesheet, and displays the main 
window of the POS system.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from frontend.main_window import POSApp
from database.database import create_db
from backend.path import get_resource_path

# Add an ID to the application in order to display the icon in the Windows taskbar
try:
    from ctypes import windll  # For Windows Users.
    myappid = 'sagravela.desktop_app.pos_system.1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

def main():
    """
    The main entry point for the POS System application.

    This function performs the following steps:
    1. Creates the database if it doesn't exist.
    2. Initializes the PyQt application.
    3. Sets the application icon.
    4. Loads and applies the stylesheet from the frontend directory.
    5. Initializes and displays the main window of the POS system.

    If the stylesheet is not found, a warning message is printed, and the application
    will use the default style instead.
    """
    # Create the database if it doesn't exist
    create_db()

    # Initialize the PyQt application
    app = QApplication(sys.argv)
    
    # Set application icon
    app.setWindowIcon(QIcon(get_resource_path(os.path.join("assets", "pos.ico"))))

    # Load stylesheet
    try:
        style_path = get_resource_path(os.path.join("frontend", "styles.qss"))
        with open(style_path, "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print(f"Warning: Could not find stylesheet at {style_path}. Using default style.")
    
    # Initialize the main window of the POS application
    window = POSApp()
    window.show()

    # Start the application's event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
