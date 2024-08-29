from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSpinBox, QSizePolicy, QSpacerItem,
    QListWidget, QPushButton, QLineEdit, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QEvent
from .utils import display_table, populate_items, filter_search, item_selected
from backend.services import save_transaction, discount_stock

class POSTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.v_layout = QVBoxLayout(self)

        # Empty widget to fill the space
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # POS Filter Search Box and Item Table display
        self.filter_search, self.item_table = display_table(self)
        
        # Connect the input search with the table
        self.filter_search.textChanged.connect(lambda: filter_search(self.filter_search, self.item_table))

        # Connect to the selection change event
        self.item_table.selectionModel().selectionChanged.connect(lambda: self.selection(self.item_table))

        # Populate items
        populate_items(self.item_table)

        # Add to layout
        self.v_layout.addWidget(self.filter_search)
        self.v_layout.addWidget(self.item_table)

        # Quantity Input
        self.quantity_layout = QHBoxLayout()
        self.quantity_label = QLabel("Quantity:")
        self.quantity_label.setObjectName("quantityLabel")
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(1000000)
        self.quantity_layout.addWidget(self.quantity_label)
        self.quantity_layout.addWidget(self.quantity_input)
        self.quantity_layout.addItem(self.spacer)
        self.v_layout.addLayout(self.quantity_layout)

        # Cart Display List
        self.cart_list = QListWidget()
        self.cart_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.v_layout.addWidget(QLabel("Cart:"))
        self.v_layout.addWidget(self.cart_list)

        # Horizontal container
        self.container = QHBoxLayout()

        # Add empty space
        self.container.addItem(self.spacer)

        # Total label
        self.total_price = QVBoxLayout()
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setObjectName("totalLabel")
        self.total_price.addItem(self.spacer)
        self.total_price.addWidget(self.total_label)
        self.total_price.addItem(self.spacer)
        self.container.addLayout(self.total_price)

        # Input for Received Amount
        self.received_amount = QVBoxLayout()
        self.received_amount_label = QLabel("Amount Received:")
        self.received_amount.addWidget(self.received_amount_label)
        self.amount = QHBoxLayout()
        self.price_label = QLabel("$")
        self.price_label.setObjectName("priceLabel")
        self.received_amount_input = QLineEdit()
        self.received_amount_input.setObjectName("receivedAmountInput")
        self.amount.addWidget(self.price_label)
        self.amount.addWidget(self.received_amount_input)
        self.amount.addItem(self.spacer)
        self.received_amount.addLayout(self.amount)
        self.received_amount.addItem(self.spacer)
        self.container.addLayout(self.received_amount)

        # Buttons
        self.button_layout = QVBoxLayout()
        self.button_layout.setObjectName("buttonLayout")

        self.add_button = QPushButton("Add to Cart")
        self.add_button.setObjectName("addToCartButton")
        self.add_button.setEnabled(False)  # Initially disable the button
        self.add_button.clicked.connect(self.add_to_cart)
        self.button_layout.addWidget(self.add_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("clearButton")
        self.clear_button.setEnabled(False)
        self.clear_button.clicked.connect(self.clear_cart)
        self.button_layout.addWidget(self.clear_button)

        self.checkout_button = QPushButton("Checkout")
        self.checkout_button.setObjectName("checkoutButton")
        self.checkout_button.setEnabled(False)
        self.checkout_button.clicked.connect(self.checkout)
        self.button_layout.addWidget(self.checkout_button)

        self.container.addLayout(self.button_layout)

        # Add empty space
        self.container.addItem(self.spacer)

        self.v_layout.addLayout(self.container)

        # Variables
        self.total_price = 0
        self.cart = []
        self.name, self.price, self.stock = None, None, None
    
    def selection(self, item_table):
        self.name, self.price, self.stock = item_selected(item_table)
        
        # Only enabled add to cart button if selected item isn't in the cart list
        if self.name not in [i[0] for i in self.cart]:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def add_to_cart(self):
        if self.name == "":
            QMessageBox.warning(self, "No Item Selected", "Please select a item from the list above.")
            return

        self.quantity = self.quantity_input.value()

        if self.quantity > self.stock:
            QMessageBox.warning(self, "Invalid Quantity", "Not enough stock. Please select a valid quantity.")
            self.quantity_input.setValue(1)
            return
        
        total_item_price = self.price * self.quantity
        self.total_price += total_item_price

        # Add the item to the cart list and the QListWidget
        self.cart.append((self.name, self.quantity))
        cart_text = f"{self.name}: {self.quantity} x ${self.price:.2f} = ${total_item_price:.2f}"
        self.cart_list.addItem(cart_text)

        # Update total label
        self.total_label.setText(f"Total: ${self.total_price:.2f}")

        # Reset the quantity input to 1
        self.quantity_input.setValue(1)

        # Enabled clear and checkout buttons
        self.clear_button.setEnabled(True)
        self.checkout_button.setEnabled(True)

        # Disabled add to cart button
        self.add_button.setEnabled(False)

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

        # Disable Checkout Button if cart list is empty
        if len(self.cart_list) == 0:
            self.checkout_button.setEnabled(False)

    def checkout(self):
        # Print cart contents to the console (could be replaced with an actual checkout process)
        try:
            self.amount_value = float(self.received_amount_input.text())
            if self.amount_value < self.total_price:
                QMessageBox.warning(self, "Insufficient Amount", "The received amount is less than the total price.")
                return

            change = self.amount_value - self.total_price
            QMessageBox.information(self, "Change to Return", f"Change to return: ${change:.2f}")
            
            # Save the transaction
            items = save_transaction(self.total_price, self.amount_value, change, self.cart)

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
            self.filter_search.clear()
            
    def eventFilter(self, source, event):
        if source == self.item_table.viewport():
            if event.type() == QEvent.Type.MouseMove:
                # Ignore mouse move events to prevent cell highlighting during scroll
                return True
        return super().eventFilter(source, event)