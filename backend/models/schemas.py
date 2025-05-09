from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# ---------- User ----------
class UserCreate(BaseModel):
    username: str
    password: str
    role_id: str

class UserOut(BaseModel):
    user_id: int
    username: str
    role_id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class LoginModel(BaseModel):
    username: str
    password: str

# ---------- Customer ----------
class CustomerBase(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]

class CustomerCreate(CustomerBase):
    pass

class CustomerOut(CustomerBase):
    customer_id: int

    class Config:
        from_attributes = True

# ---------- Supplier ----------
class SupplierBase(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]

class SupplierCreate(SupplierBase):
    pass

class SupplierOut(SupplierBase):
    supplier_id: int

    class Config:
        from_attributes = True

# ---------- Product ----------
class ProductBase(BaseModel):
    name: str
    category: Optional[str]
    price: float
    supplier_id: Optional[int]

class ProductCreate(ProductBase):
    pass

class ProductOut(BaseModel):
    product_id: int
    name: str
    category: Optional[str] = None
    price: float
    supplier_id: Optional[int] = None

    class Config:
        from_attributes = True

# ---------- Stock ----------
class StockCreate(BaseModel):
    product_id: int
    quantity: int

class StockBase(BaseModel):
    product_id: int
    quantity: int

class StockOut(StockBase):
    stock_id: int
    last_updated: datetime

    class Config:
        from_attributes = True

# ---------- Order & Order Items ----------
class OrderItem(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    customer_id: int
    order_date: date
    status: str

class OrderOut(BaseModel):
    order_id: int
    customer_id: int
    order_date: date
    status: str

    class Config:
        from_attributes = True

class OrderItemOut(BaseModel):
    order_item_id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

# ---------- Invoice ----------
class InvoiceCreate(BaseModel):
    order_id: int
    invoice_date: date
    total_amount: float
    payment_status: Optional[str] = "Pending"

class InvoiceOut(BaseModel):
    invoice_id: int
    order_id: int
    invoice_date: date
    total_amount: float
    payment_status: str

    class Config:
        from_attributes = True

# ---------- Shipping ----------
class ShippingCreate(BaseModel):
    invoice_id: int
    shipping_date: date
    shipping_status: str

class ShippingOut(BaseModel):
    shipping_id: int
    invoice_id: int
    shipping_date: date
    shipping_status: str

    class Config:
        from_attributes = True

# testing if schemas work with the main backend code
if __name__ == "__main__":
    test = ShippingOut(
        shipping_id=1,
        invoice_id=101,
        shipping_date=date.today(),
        shipping_status="Shipped"
    )
    print(test.model_dump_json())