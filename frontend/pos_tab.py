from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSpinBox, 
    QListWidget, QPushButton, QLineEdit, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from .utils import display_table, populate_items, filter_search, item_selected
from backend.services import save_transaction, discount_stock

class POSTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # POS Filter Search Box and Item Table display
        self.filter_search, self.item_table = display_table(self)
        
        # Selected element label
        self.selected_label = QLabel("Selected Item: None", parent)
        
        # Connect the input search with the table
        self.filter_search.textChanged.connect(lambda: filter_search(self.filter_search, self.item_table))

        # Connect to the selection change event
        self.item_table.selectionModel().selectionChanged.connect(lambda: self.selection(self.item_table, self.selected_label))

        # Populate items
        populate_items(self.item_table)

        # Add to layout
        self.layout.addWidget(QLabel("Search Item:"))
        self.layout.addWidget(self.filter_search)
        self.layout.addWidget(QLabel("Items:"))
        self.layout.addWidget(self.item_table)        
        self.layout.addWidget(self.selected_label)

        # Quantity Input
        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(1000000)
        self.layout.addWidget(self.quantity_label)
        self.layout.addWidget(self.quantity_input)

        # Cart Display List
        self.cart_list = QListWidget()
        self.cart_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.layout.addWidget(QLabel("Cart:"))
        self.layout.addWidget(self.cart_list)

        # Total label
        self.total_label = QLabel("Total: $0.00")
        self.layout.addWidget(self.total_label)

        # Input for Received Amount
        self.received_amount_label = QLabel("Amount Received:")
        self.layout.addWidget(self.received_amount_label)
        self.received_amount_input = QLineEdit()
        self.layout.addWidget(self.received_amount_input)

        # Buttons
        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add to Cart")
        self.add_button.clicked.connect(self.add_to_cart)
        self.button_layout.addWidget(self.add_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_cart)
        self.button_layout.addWidget(self.clear_button)

        self.checkout_button = QPushButton("Checkout")
        self.checkout_button.clicked.connect(self.checkout)
        self.button_layout.addWidget(self.checkout_button)

        self.layout.addLayout(self.button_layout)

        # Variables
        self.total_price = 0
        self.cart = []
    
    def selection(self, item_table, selected_label):
        self.name, self.price, self.stock = item_selected(item_table)
        selected_label.setText(f"Selected Item: {self.name}  ${self.price}")

    def add_to_cart(self):
        if self.name is None:
            QMessageBox.warning(self, "No Item Selected", "Please select a item from the list above.")
            return

        quantity = self.quantity_input.value()

        if quantity > self.stock:
            QMessageBox.warning(self, "Invalid Quantity", "Not enough stock. Please select a valid quantity.")
            self.quantity_input.setValue(1)
            return
        
        total_item_price = self.price * quantity
        self.total_price += total_item_price
        cart_item = (self.name, self.price, quantity, total_item_price)

        # Add the item to the cart list and the QListWidget
        self.cart.append(cart_item)
        cart_text = f"{self.name}: {quantity} x ${self.price:.2f} = ${total_item_price:.2f}"
        self.cart_list.addItem(cart_text)

        # Update total label
        self.total_label.setText(f"Total: ${self.total_price:.2f}")
        self.selected_label.setText("Selected Item:")

        # Reset the quantity input to 1
        self.quantity_input.setValue(1)

    def clear_cart(self):
        selected_items = self.cart_list.selectedItems()
        
        if selected_items:
            # Clear only selected items
            for item in selected_items:
                self.cart_list.takeItem(self.cart_list.row(item))
            self.cart_list.clearSelection()  # Unselect all items in the cart list
        else:
            # Clear all items
            self.total_price = 0.0
            self.cart.clear()
            self.cart_list.clear()
            self.total_label.setText("Total: $0.00")

    def checkout(self):
        # Print cart contents to the console (could be replaced with an actual checkout process)
        try:
            received_amount = float(self.received_amount_input.text())
            if received_amount < self.total_price:
                QMessageBox.warning(self, "Insufficient Amount", "The received amount is less than the total price.")
                return

            change = received_amount - self.total_price
            QMessageBox.information(self, "Change to Return", f"Change to return: ${change:.2f}")
            
            # Save the transaction
            items = save_transaction(self.total_price, received_amount, change, self.cart)

            # Discount stock
            discount_stock(items)

            # Refresh the table
            populate_items(self.item_table)

            # Clear the amount received input and cart after checkout
            self.received_amount_input.clear()
            self.clear_cart()

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the received amount.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.cart_list.clearSelection()