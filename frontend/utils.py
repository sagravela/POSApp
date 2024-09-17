from PyQt6.QtWidgets import QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from PyQt6.QtCore import Qt
from backend.services import get_items

def display_table(parent: QWidget):
    """
    Creates a search input and item table for displaying store items.

    This function sets up a QLineEdit widget for filtering items and a QTableWidget
    for displaying store items with three columns: Item, Price, and Stock. The table
    is sortable, supports single-row selection, and automatically resizes columns
    to fit the content. An event filter is installed to handle scroll events within
    the table's viewport.

    Parameters
    ----------
    parent : QWidget
        The parent widget to which the table and search bar will be added.

    Returns
    -------
    tuple
        A tuple containing the QLineEdit for filtering items and the QTableWidget for displaying items.
    """
    filter_search = QLineEdit(parent)
    filter_search.setPlaceholderText("Search for a item...")

    item_table = QTableWidget(parent)
    item_table.setColumnCount(3)
    item_table.setHorizontalHeaderLabels(["Item", "Price", "Stock"])
    item_table.verticalHeader().setVisible(False)
    item_table.horizontalHeader().setStretchLastSection(True)
    item_table.setSortingEnabled(True)
    
    header = item_table.horizontalHeader()
    for index in range(item_table.columnCount()):
        header.setSectionResizeMode(index, QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)

    item_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    item_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)  

    # Install event filter to handle wheel events
    # item_table.viewport().installEventFilter(parent)

    return filter_search, item_table

def populate_table(item_table: QTableWidget):
    """
    Populates the item table with store data.

    This function retrieves the store's item data and adds it to the item table.
    Each row contains the item's name, price, and stock. 
    The table is cleared before inserting new rows, and items are marked
    as selectable but not editable.

    Parameters
    ----------
    item_table : QTableWidget
        The table widget where the items will be displayed.
    """
    data = get_items()
    item_table.setRowCount(0)
    for row, (store, item) in enumerate(data):
        item_table.insertRow(row)
        name_item = QTableWidgetItem(item.name)
        price_item = QTableWidgetItem()
        stock_item = QTableWidgetItem()
        price_item.setData(Qt.ItemDataRole.DisplayRole, round(item.price, 2))
        stock_item.setData(Qt.ItemDataRole.DisplayRole, store.stock)

        name_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        price_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        stock_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        item_table.setItem(row, 0, name_item)
        item_table.setItem(row, 1, price_item)
        item_table.setItem(row, 2, stock_item)

def filter_search(input: QLineEdit, table: QTableWidget):
    """
    Filters the item table based on user input.

    This function filters the rows of the item table according to the text entered
    in the search bar. Only rows whose item name contains the search text (case-insensitive)
    will remain visible.

    Parameters
    ----------
    input : QLineEdit
        The search bar where the user types the filter text.
    table : QTableWidget
        The table widget whose rows will be filtered based on the search text.
    """
    filter_text = input.text().lower()
    if table:
        for row in range(table.rowCount()):
            item_item = table.item(row, 0)
            if filter_text in item_item.text().lower():
                table.setRowHidden(row, False)
            else:
                table.setRowHidden(row, True)

def item_selected(item_table: QTableWidget):
    """
    Retrieves the selected item's details from the table.

    This function returns the name, price, and stock of the currently selected row
    in the item table. If no row is selected, it returns empty values.

    Parameters
    ----------
    item_table : QTableWidget
        The table widget containing the item data.

    Returns
    -------
    tuple
        A tuple containing the name (str), price (float), and stock (int) of the selected item.
        If no item is selected, an empty tuple is returned.
    """
    selected_rows = item_table.selectionModel().selectedRows()
    if selected_rows:
        row = selected_rows[0].row()
        name = item_table.item(row, 0).text()
        price = float(item_table.item(row, 1).text())
        stock = int(item_table.item(row, 2).text())
        return name, price, stock
    return "", "", ""
