from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from backend.models.schemas import OrderCreate, OrderOut
from backend.auth.role_checker import JWTBearer
from backend.database import get_connection
import pymysql

router = APIRouter()

# Create a new order
@router.post("/orders", response_model=OrderOut, dependencies=[Depends(JWTBearer(["admin", "manager", "staff", "customer"]))])
def create_order(order: OrderCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO orders (customer_id, order_date, status) VALUES (%s, %s, %s)",
            (order.customer_id, order.order_date, order.status)
        )
        conn.commit()
        order_id = cursor.lastrowid
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=500, detail="Failed to retrieve the created order.")
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))
    finally:
        cursor.close()
        conn.close()

# Get all orders
@router.get("/orders", response_model=List[OrderOut], dependencies=[Depends(JWTBearer(["admin", "manager", "staff", "customer"]))])
def get_orders():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()
        conn.close()

# Get order by ID
@router.get("/orders/{order_id}", response_model=OrderOut, dependencies=[Depends(JWTBearer(["admin", "manager", "staff", "customer"]))])
def get_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))
    finally:
        cursor.close()
        conn.close()

# Update an order
@router.put("/orders/{order_id}", response_model=OrderOut, dependencies=[Depends(JWTBearer(["admin", "manager", "staff", "customer"]))])
def update_order(order_id: int, order: OrderCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE orders SET customer_id=%s, order_date=%s, status=%s WHERE order_id=%s",
            (order.customer_id, order.order_date, order.status, order_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found or not updated")
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        row = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))
    finally:
        cursor.close()
        conn.close()

# Delete an order
@router.delete("/orders/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer(["admin", "manager", "staff", "customer"]))])
def delete_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order deleted successfully"}
    finally:
        cursor.close()
        conn.close()
