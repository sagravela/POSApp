import sys, os
from PyQt6.QtWidgets import QApplication
from frontend.main_window import POSApp
from database.database import create_db

if __name__ == '__main__':
    create_db()  # Create the database tables

    app = QApplication(sys.argv)
    
    # Load stylesheet
    with open(os.path.join("frontend", "styles.qss"), "r") as file:
        app.setStyleSheet(file.read())
    
    window = POSApp()
    window.show()
    sys.exit(app.exec())
