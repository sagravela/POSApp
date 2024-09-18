# POSApp

**POSApp** is a comprehensive Point of Sale (POS) system designed to streamline inventory management, transaction processing, and sales reporting. Developed as a Windows desktop application, it offers an easy installation process and an intuitive user interface. Built with PyQt6, **POSApp** provides a seamless experience for bar and restaurant management, as well as other small businesses. Key features include:

- **Product Management**: Add and update products, track inventory levels.
- **Transaction Processing**: Efficiently handle sales, calculate totals, and manage payments.
- **Analytics and Reporting**: View detailed sales reports and visualize data through interactive charts.

With its user-friendly design and robust functionality, **POSApp** helps businesses manage their operations effectively and gain valuable insights into their sales and inventory.

## Features

- **POS System Tab**: Process sales transactions, view cart items, and calculate totals and change.
- **Add Product Tab**: Add new products to the inventory and update existing ones.
- **Analytics Tab**: Visualize sales data and inventory statistics with charts.
- **Dynamic Plotting**: View most and least sold items with horizontal bar charts.
- **Database Integration**: Uses SQLAlchemy for database operations, with SQLite as the backend.
- **Windows Installer**: Bundled with *PyInstaller* and setup installer created using *InstallForge* for easy installation on Windows.

## Installation

Download `POSApp_setup.exe` file from this [drive folder](https://drive.google.com/drive/folders/1DFYtDMS6kZp845ri0G5G6KCga50GiskE?usp=sharing) and follow the steps given by the installer.

## Usage

1. **POS System Tab**:
    - Add items to the cart.
    - Process transactions by entering the total amount, received payment, and change to be returned.

2. **Add Product Tab**:
    - Enter product details and add them to the inventory.
    - Update existing product details and stock.

3. **Analytics Tab**:
    - Charts show total sales over time, most sold items, and least sold items.

## Configuration

- **Database Path**: The database file is stored locally in the user's home directory as `.pos_inventory.db`.
- **PyInstaller Spec**: The `pos.spec` file define the configuration for the bundled program.
