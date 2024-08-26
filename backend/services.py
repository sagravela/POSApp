from database.database import get_session
from database.models import Items, Store, Transaction, TransactionItem

def get_items():
    session = get_session()
    results = session.query(Store, Items).join(Items, Items.id == Store.item_id).all()
    session.close()
    return results

def save_transaction(total, amount, change, cart):
    # Create a new transaction
    session = get_session()
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
        item, price, quantity, total_item_price = item
        item_id = item_id_map.get(item)
        items[item_id] = quantity
        transaction_item = TransactionItem(
            transaction_id=transaction.id,
            item_id=item_id,
            quantity=quantity,
        )
        session.add(transaction_item)

    session.commit()
    session.close()
    return items

def discount_stock(items: dict):
    session = get_session()
    for item_id, quantity in items.items():
        # Retrieve the POS entry for the given item_id
        store_item = session.query(Store).filter_by(item_id=item_id).first()
        
        # Subtract the quantity from stock
        store_item.stock -= quantity
            
        # Commit the changes to the database
        session.commit()
    session.close()

def save_item(name: str, price: float, stock: int):
    session = get_session()
    item_data = session.query(Items).filter_by(name=name).first()
    try:
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
                raise Exception(f"Item with ID {item_data.id} not found.")
        else:
            # Add a new item
            new_item = Items(name=name, price=price)
            session.add(new_item)
            session.commit()  # Commit to get the new item's ID

            new_pos_entry = Store(item_id=new_item.id, stock=stock)
            session.add(new_pos_entry)
            session.commit()  # Commit the new entry

    except Exception as e:
        session.rollback()  # Rollback in case of any errors
        raise e
    finally:
        session.close()

def remove_item_by_name(name: str):
    session = get_session()
    try:
        # Find the item by name
        item = session.query(Items).filter(Items.name == name).first()
        
        if item:
            # Delete the corresponding entry in the Store table
            session.query(Store).filter(Store.item_id == item.id).delete()

            # Delete the item itself
            session.delete(item)
            session.commit()
        else:
            print(f"Item with name {name} not found.")

    except Exception as e:
        session.rollback()  # Rollback in case of any errors
        print(f"An error occurred: {e}")
    finally:
        session.close()

