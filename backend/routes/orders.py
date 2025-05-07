from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import OrderCreate, OrderOut
from backend.auth.role_checker import JWTBearer
from backend.database import get_connection

router = APIRouter()

# Create a new order
@router.post("/orders", response_model=OrderOut, dependencies=[Depends(JWTBearer(["admin", "manager", "staff", "customer"]))])
def create_order(order: OrderCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO orders (customer_id, order_date, status) VALUES (%s, %s, %s)",
            (order.customer_id, order.order_date, order.status)
        )
        conn.commit()
        cursor.execute("SELECT * FROM orders WHERE order_id = LAST_INSERT_ID()")
        new_order = cursor.fetchone()
        return new_order
    finally:
        cursor.close()
        conn.close()

# Get all orders
@router.get("/orders", response_model=List[OrderOut], dependencies=[Depends(JWTBearer(["admin", "manager", "staff", "customer"]))])
def get_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        return orders
    finally:
        cursor.close()
        conn.close()

# Get order by ID
@router.get("/orders/{order_id}", response_model=OrderOut, dependencies=[Depends(JWTBearer(["admin", "manager", "staff", "customer"]))])
def get_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    finally:
        cursor.close()
        conn.close()

# Update an order
@router.put("/orders/{order_id}", response_model=OrderOut, dependencies=[Depends(JWTBearer(["admin", "manager", "staff", "customer"]))])
def update_order(order_id: int, order: OrderCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "UPDATE orders SET customer_id=%s, order_date=%s, status=%s WHERE order_id=%s",
            (order.customer_id, order.order_date, order.status, order_id)
        )
        conn.commit()
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        updated_order = cursor.fetchone()
        return updated_order
    finally:
        cursor.close()
        conn.close()

# Delete an order
@router.delete("/orders/{order_id}", dependencies=[Depends(JWTBearer(["admin", "manager", "staff", "customer"]))])
def delete_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        conn.commit()
        return {"message": "Order deleted successfully"}
    finally:
        cursor.close()
        conn.close()