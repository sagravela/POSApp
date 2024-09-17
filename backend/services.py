from database.database import get_session
from database.models import Items, Store, Transaction, TransactionItem
from sqlalchemy import func
from datetime import datetime

def get_items():
    """
    Retrieves a list of items along with their stock information.

    This function queries the database for all items and their associated stock levels. 
    It joins the `Store` and `Items` tables to obtain this information.

    Returns
    -------
    list of tuple
        A list of tuples where each tuple contains information from both `Store` and `Items` tables.
    """
    with get_session() as session:
        results = session.query(Store, Items).join(Items, Items.id == Store.item_id).all()
    return results

def get_transactions():
    """
    Retrieves aggregated sales data by day.

    This function queries the database for total sales amount grouped by day. 
    It aggregates the sales data and formats the results for plotting.

    Returns
    -------
    tuple of (list of datetime, list of float)
        - A list of dates.
        - A list of total sales amounts corresponding to each date.
    """
    with get_session() as session:
        results = session.query(
            func.date(Transaction.timestamp).label('date'),
            func.sum(Transaction.total_amount).label('total_sales')
        ).group_by(func.date(Transaction.timestamp)).order_by(func.date(Transaction.timestamp)).all()

    # Extract dates and sales from results
    dates = [datetime.strptime(result.date, '%Y-%m-%d') for result in results]
    total_sales = [result.total_sales for result in results]
    
    return dates, total_sales

def sold_items_sorted():
    """
    Retrieves and sorts items by the total quantity sold.

    This function returns a list of items along with their total quantities sold, sorted in ascending order by quantity.

    Returns
    -------
    list of tuple
        A list of tuples where each tuple contains the item name and its total quantity sold.
    """
    with get_session() as session:
        return (
            session.query(
                Items.name.label('item_name'),
                func.sum(TransactionItem.quantity).label('total_quantity')
            )
            .join(Items, TransactionItem.item_id == Items.id)
            .group_by(Items.name)
            .order_by(func.sum(TransactionItem.quantity))
            .all()
        )
    
def save_transaction(total: float, amount: float, change: float, cart: list[tuple]):
    """
    Saves a new transaction along with its associated items to the database.

    This function creates a new transaction entry, saves it to the database, and 
    then adds each item in the cart to the `TransactionItem` table. 

    Parameters
    ----------
    total : float
        The total amount for the transaction.
    amount : float
        The amount of payment received.
    change : float
        The amount of change to be returned.
    cart : list of tuple
        A list of tuples where each tuple contains the item name and quantity.

    Returns
    -------
    dict
        A dictionary mapping item IDs to quantities for the items in the cart.
    """
    # Create a new transaction
    with get_session() as session:
        transaction = Transaction(
            total_amount=total,
            payment_received=amount,
            change_returned=change
        )
        session.add(transaction)
        session.commit()

        # Fetch all items with stock to create a mapping
        item_data = session.query(Items).all()
        item_id_map = {item.name: item.id for item in item_data}

        # Add transaction items
        items = {}
        for item in cart:
            name, quantity = item
            item_id = item_id_map.get(name)
            items[item_id] = quantity
            transaction_item = TransactionItem(
                transaction_id=transaction.id,
                item_id=item_id,
                quantity=quantity,
            )
            session.add(transaction_item)

        session.commit()

    return items

def discount_stock(items: dict):
    """
    Updates the stock quantities based on the items sold in a transaction.

    This function subtracts the specified quantities of items from the stock. 
    It updates the `Store` table to reflect the new stock levels.

    Parameters
    ----------
    items : dict
        A dictionary where keys are item IDs and values are quantities to be subtracted from the stock.

    Returns
    -------
    None
    """
    with get_session() as session:
        for item_id, quantity in items.items():
            # Retrieve the POS entry for the given item_id
            store_item = session.query(Store).filter_by(item_id=item_id).first()
            
            # Subtract the quantity from stock
            store_item.stock -= quantity
                
            # Commit the changes to the database
            session.commit()

def save_item(name: str, price: float, stock: int):
    """
    Adds a new item to the database or updates an existing item's details.

    This function checks if an item with the given name exists. If it does, it updates the item's 
    price and stock information. If it does not exist, it creates a new item and adds it to the database.

    Parameters
    ----------
    name : str
        The name of the item.
    price : float
        The price of the item.
    stock : int
        The quantity of the item in stock.

    Returns
    -------
    None
    """
    with get_session() as session:
        item_data = session.query(Items).filter_by(name=name).first()
        if item_data:
            # Update existing item
            item = session.query(Items).filter_by(id=item_data.id).first()
            if item:
                item.name = name
                item.price = price

                store_entry = session.query(Store).filter_by(item_id=item_data.id).first()
                if store_entry:
                    store_entry.stock = stock

                session.commit()  # Commit the updates
        else:
            # Add a new item
            new_item = Items(name=name, price=price)
            session.add(new_item)
            session.commit()  # Commit to get the new item's ID

            new_pos_entry = Store(item_id=new_item.id, stock=stock)
            session.add(new_pos_entry)
            session.commit()  # Commit the new entry

def remove_item_by_name(name: str):
    """
    Removes an item and its associated stock entry from the database.

    This function deletes the item with the specified name from both the `Items` and `Store` tables.

    Parameters
    ----------
    name : str
        The name of the item to be removed.

    Returns
    -------
    None
    """
    with get_session() as session:
        # Find the item by name
        item = session.query(Items).filter(Items.name == name).first()

        # Delete the corresponding entry in the Store table
        session.query(Store).filter(Store.item_id == item.id).delete()

        # Delete the item itself
        session.delete(item)
        session.commit()
