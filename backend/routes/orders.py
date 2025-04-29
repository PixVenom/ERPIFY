from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import OrderCreate, OrderOut
from backend.auth.role_checker import manager_required
from backend.utils.db import get_connection

router = APIRouter()


@router.post("/orders", response_model=OrderOut, dependencies=[Depends(manager_required)])
def create_order(order: OrderCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO orders (CustomerID, OrderDate, Status) VALUES (%s, %s, %s)",
                   (order.customer_id, order.order_date, order.status))
    conn.commit()
    cursor.execute("SELECT * FROM orders WHERE OrderID = LAST_INSERT_ID()")
    new_order = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_order


@router.get("/orders", response_model=List[OrderOut], dependencies=[Depends(manager_required)])
def get_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders


@router.get("/orders/{order_id}", response_model=OrderOut, dependencies=[Depends(manager_required)])
def get_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE OrderID = %s", (order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=OrderOut, dependencies=[Depends(manager_required)])
def update_order(order_id: int, order: OrderCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE orders SET CustomerID=%s, OrderDate=%s, Status=%s WHERE OrderID=%s",
                   (order.customer_id, order.order_date, order.status, order_id))
    conn.commit()
    cursor.execute("SELECT * FROM orders WHERE OrderID = %s", (order_id,))
    updated_order = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_order


@router.delete("/orders/{order_id}", dependencies=[Depends(manager_required)])
def delete_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE OrderID = %s", (order_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Order deleted successfully"}
