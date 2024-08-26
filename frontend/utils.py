from PyQt6.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PyQt6.QtCore import Qt
from backend.services import get_items

def display_table(parent):
    filter_search = QLineEdit(parent)
    filter_search.setPlaceholderText("Search for a item...")

    item_table = QTableWidget(parent)
    item_table.setColumnCount(3)
    item_table.setHorizontalHeaderLabels(["Item", "Price", "Stock"])
    item_table.verticalHeader().setVisible(False)
    item_table.horizontalHeader().setStretchLastSection(True)

    header = item_table.horizontalHeader()
    for index in range(item_table.columnCount()):
        header.setSectionResizeMode(index, QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)

    item_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    item_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
    return filter_search, item_table

def populate_items(item_table):
    data = get_items()
    item_table.setRowCount(0)
    for row, (store, item) in enumerate(data):
        item_table.insertRow(row)
        name_item = QTableWidgetItem(item.name)
        price_item = QTableWidgetItem(f"{item.price:.2f}")
        stock_item = QTableWidgetItem(str(store.stock))
        
        name_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        price_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        stock_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        item_table.setItem(row, 0, name_item)
        item_table.setItem(row, 1, price_item)
        item_table.setItem(row, 2, stock_item)

def filter_search(input, table):
    filter_text = input.text().lower()
    if table:
        for row in range(table.rowCount()):
            item_item = table.item(row, 0)
            if filter_text in item_item.text().lower():
                table.setRowHidden(row, False)
            else:
                table.setRowHidden(row, True)

def item_selected(item_table):
    selected_rows = item_table.selectionModel().selectedRows()
    if selected_rows:
        row = selected_rows[0].row()
        name = item_table.item(row, 0).text()
        price = float(item_table.item(row, 1).text().replace('$', ''))
        stock = int(item_table.item(row, 2).text())
        return name, price, stock
    return "", "", ""
