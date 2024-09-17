from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import QLocale
from .pos_tab import POSTab
from .store_tab import StoreTab
from .analytics import AnalyticsTab
from .utils import populate_table

class POSApp(QMainWindow):
    """
    The POSApp class represents the main window of the Point of Sale (POS) System.
    """

    def __init__(self):
        """
        Initializes the main window of the POSApp.

        Sets the window title, size, and locale. Initializes the main widget and
        the three primary tabs (POS, Store, Analytics). The layout and tab system 
        are set up within the central widget, and the tab change event is connected 
        to the `refresh_current_tab` method.
        """
        super().__init__()
        self.setWindowTitle("Point of Sale System")

        # Fix the size of the window to 1280x720
        self.setGeometry(100, 100, 1280, 720)

        # Set application locale to ensure dot as decimal separator
        QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))

        # Main widget to contain everything
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Create the tabs widget
        self.tabs = QTabWidget(self.main_widget)

        # Add tabs
        self.pos_tab = POSTab(self)
        self.tabs.addTab(self.pos_tab, "POS")

        self.store_tab = StoreTab(self)
        self.tabs.addTab(self.store_tab, "Store")

        self.analytics_tab = AnalyticsTab(self)
        self.tabs.addTab(self.analytics_tab, "Analytics")

        # Refresh the tab content after tab is changed
        self.tabs.currentChanged.connect(self.refresh_current_tab)

        # Main layout inside the main widget
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.addWidget(self.tabs)

    def refresh_current_tab(self, index):
        """
        Refreshes the content of the current tab when it is selected.

        This method is triggered when the user switches between tabs. Depending on the
        index of the currently selected tab, it refreshes the content by repopulating
        the item table for POS and Store tabs, or redrawing the analytics chart.

        Parameters
        ----------
        index : int
            The index of the currently selected tab (0 for POS, 1 for Store, 2 for Analytics).
        """
        if index == 0:
            self.pos_tab.refresh()
        elif index == 1:
            self.store_tab.refresh()
        elif index == 2:
            self.analytics_tab.redraw()
