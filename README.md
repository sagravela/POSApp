# POSApp

**POSApp** is a comprehensive Point of Sale (POS) system designed to streamline inventory management, transaction processing, and sales reporting. Developed as a Windows desktop application, it offers an easy installation process and an intuitive user interface. Built with PyQt6, **POSApp** provides a seamless experience for bar and restaurant management, as well as other small businesses. Key features include:

- **Product Management**: Add and update products, track inventory levels.
- **Transaction Processing**: Efficiently handle sales, calculate totals, and manage payments.
- **Analytics and Reporting**: View detailed sales reports and visualize data through interactive charts.

With its user-friendly design and robust functionality, **POSApp** helps businesses manage their operations effectively and gain valuable insights into their sales and inventory.

![POSApp Gif](assets\captures\posapp.gif)

## Features

- **POS System Tab**: Process sales transactions, view cart items, and calculate totals and change.
- **Add Product Tab**: Add new products to the inventory and update existing ones.
- **Analytics Tab**: Visualize sales data and inventory statistics with charts.
- **Dynamic Plotting**: View most and least sold items with horizontal bar charts.
- **Database Integration**: Uses SQLAlchemy for database operations, with SQLite as the backend.
- **Windows Installer**: Bundled with *PyInstaller* and setup installer created using *InstallForge* for easy installation on Windows.

## Installation

Download setup from [drive](https://drive.google.com/file/d/13LjpoL5892c4EIVMrnrFJc7Y_U_l1vbk/view?usp=drive_link) and follow the steps given by the installer.

### **Important Note**

When installing the program, you may see a warning from Windows indicating that the file is from an "unknown publisher" or that it might be flagged as a potentially unwanted application. This happens because the installer has not been digitally signed with a certificate that Windows recognizes, which is a common occurrence for software created by independent developers or small teams.

However, **you can trust this application**:

- It was developed with care to assist in managing your Point of Sale operations.
- The file has been scanned for malware and is safe to install.
- If you have any doubts, feel free to contact me for verification.

#### **Steps to Bypass the Warning**

1. When the warning appears, click on **"More info"**.
2. Select **"Run anyway"** to proceed with the installation.

By following these steps, you can safely install and use the POSApp.

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
