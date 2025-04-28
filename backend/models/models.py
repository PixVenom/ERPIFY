from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ---------- User ----------
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    created_at = Column(DateTime, nullable=False)

    role = relationship("Role", back_populates="users")

# ---------- Role ----------
class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    users = relationship("User", back_populates="role")

# ---------- Customer ----------
class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)

# ---------- Supplier ----------
class Supplier(Base):
    __tablename__ = 'suppliers'
    supplier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)

# ---------- Product ----------
class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String, nullable=True)
    price = Column(Float)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=True)

    supplier = relationship("Supplier")

# ---------- Stock ----------
class Stock(Base):
    __tablename__ = 'stocks'
    stock_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer)
    last_updated = Column(DateTime)

    product = relationship("Product")

# ---------- Order & Order Items ----------
class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    order_date = Column(Date)
    status = Column(String)

    customer = relationship("Customer")

class OrderItem(Base):
    __tablename__ = 'order_items'
    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer)
    unit_price = Column(Float)

    order = relationship("Order")
    product = relationship("Product")

# ---------- Invoice ----------
class Invoice(Base):
    __tablename__ = 'invoices'
    invoice_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    invoice_date = Column(Date)
    total_amount = Column(Float)
    payment_status = Column(String, default="Pending")

    order = relationship("Order")