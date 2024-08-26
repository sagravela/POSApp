from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import QLocale, QEvent
from .pos_tab import POSTab
from .store_tab import StoreTab

class POSApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Point of Sale System")
        self.setGeometry(100, 100, 800, 600)

        # Set application locale to ensure dot as decimal separator
        QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))

        # Main widget to contain everything
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Create the tab widget
        self.tabs = QTabWidget(self.main_widget)

        # Add tabs
        self.pos_tab = POSTab(self)
        self.tabs.addTab(self.pos_tab, "POS")

        self.store_tab = StoreTab(self)
        self.tabs.addTab(self.store_tab, "Store")

        # Main layout inside the main widget
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.addWidget(self.tabs)
