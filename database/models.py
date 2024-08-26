from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # Relationships to Store and POS
    stores = relationship("Store", back_populates="item")

class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    stock = Column(Integer, default=0, nullable=False)

    # Relationship to Items
    item = relationship("Items", back_populates="stores")

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    payment_received = Column(Float, nullable=False)
    change_returned = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())

    # Relationship to TransactionItems
    transaction = relationship("TransactionItem", back_populates="items")

class TransactionItem(Base):
    __tablename__ = 'transaction_items'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationships
    items = relationship("Transaction", back_populates="transaction")
    item = relationship("Items")
