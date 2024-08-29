from database.database import get_session
from database.models import Items, Store, Transaction, TransactionItem
from sqlalchemy import func
from datetime import datetime

def get_items():
    with get_session() as session:
        results = session.query(Store, Items).join(Items, Items.id == Store.item_id).all()
    return results

def get_transactions():
    # Using a context manager for session management
    with get_session() as session:
        results = session.query(
            func.date(Transaction.timestamp).label('date'),
            func.sum(Transaction.total_amount).label('total_sales')
        ).group_by(func.date(Transaction.timestamp)).order_by(func.date(Transaction.timestamp)).all()

    # Extract dates and sales from results
    dates = [datetime.strptime(result.date, '%Y-%m-%d') for result in results]
    total_sales = [result.total_sales for result in results]
    
    return dates, total_sales

def get_most_items():
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
    
def save_transaction(total, amount, change, cart):
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
            item, quantity = item
            item_id = item_id_map.get(item)
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
    with get_session() as session:
        for item_id, quantity in items.items():
            # Retrieve the POS entry for the given item_id
            store_item = session.query(Store).filter_by(item_id=item_id).first()
            
            # Subtract the quantity from stock
            store_item.stock -= quantity
                
            # Commit the changes to the database
            session.commit()


def save_item(name: str, price: float, stock: int):
    item_data = session.query(Items).filter_by(name=name).first()
    with get_session() as session:
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
    with get_session() as session:
        # Find the item by name
        item = session.query(Items).filter(Items.name == name).first()

        # Delete the corresponding entry in the Store table
        session.query(Store).filter(Store.item_id == item.id).delete()

        # Delete the item itself
        session.delete(item)
        session.commit()

