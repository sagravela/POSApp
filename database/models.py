from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base class for all the models
Base = declarative_base()

class Items(Base):
    """
    The Items class represents the items available in the store.

    Attributes
    ----------
    id : int
        Primary key of the Items table.
    name : str
        The name of the item.
    price : float
        The price of the item.

    Relationships
    -------------
    stores : list of Store
        A list of Store objects that indicates the inventory of this item.
    """
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)

    # Relationships to Store and POS
    stores = relationship("Store", back_populates="item")

class Store(Base):
    """
    The Store class represents the inventory of items in stock.

    Attributes
    ----------
    id : int
        Primary key of the Store table.
    item_id : int
        Foreign key linking to the Items table.
    stock : int
        The quantity of the item available in stock.

    Relationships
    -------------
    item : Items
        The corresponding item from the Items table.
    """
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    stock = Column(Integer, default=0, nullable=False)

    # Relationship to Items
    item = relationship("Items", back_populates="stores")

class Transaction(Base):
    """
    The Transaction class represents a sales transaction.

    Attributes
    ----------
    id : int
        Primary key of the Transactions table.
    total_amount : float
        The total amount of the transaction.
    payment_received : float
        The amount of money received from the customer.
    change_returned : float
        The amount of change returned to the customer.
    timestamp : datetime
        The date and time when the transaction was made, with a default of the current time.

    Relationships
    -------------
    transaction : list of TransactionItem
        A list of TransactionItem objects that represent the items involved in the transaction.
    """
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    payment_received = Column(Float, nullable=False)
    change_returned = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())

    # Relationship to TransactionItems
    transaction = relationship("TransactionItem", back_populates="items")

class TransactionItem(Base):
    """
    The TransactionItem class represents the items involved in a transaction.

    Attributes
    ----------
    id : int
        Primary key of the TransactionItems table.
    transaction_id : int
        Foreign key linking to the Transactions table.
    item_id : int
        Foreign key linking to the Items table.
    quantity : int
        The quantity of the item involved in the transaction.

    Relationships
    -------------
    items : Transaction
        The associated transaction from the Transactions table.
    item : Items
        The corresponding item from the Items table.
    """
    __tablename__ = 'transaction_items'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationships
    items = relationship("Transaction", back_populates="transaction")
    item = relationship("Items")
