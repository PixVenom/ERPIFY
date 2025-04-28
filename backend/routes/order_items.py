from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.schemas import OrderItemCreate, OrderItemOut
from auth.role_checker import manager_required
from backend.utils.db import get_connection

router = APIRouter()


@router.post("/order_items", response_model=OrderItemOut, dependencies=[Depends(manager_required)])
def create_order_item(order_item: OrderItemCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice) VALUES (%s, %s, %s, %s)",
                   (order_item.order_id, order_item.product_id, order_item.quantity, order_item.unit_price))
    conn.commit()
    cursor.execute("SELECT * FROM OrderItems WHERE OrderItemID = LAST_INSERT_ID()")
    new_order_item = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_order_item


@router.get("/order_items", response_model=List[OrderItemOut], dependencies=[Depends(manager_required)])
def get_order_items():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM OrderItems")
    order_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return order_items


@router.get("/order_items/{order_item_id}", response_model=OrderItemOut, dependencies=[Depends(manager_required)])
def get_order_item(order_item_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM OrderItems WHERE OrderItemID = %s", (order_item_id,))
    order_item = cursor.fetchone()
    cursor.close()
    conn.close()
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item


@router.put("/order_items/{order_item_id}", response_model=OrderItemOut, dependencies=[Depends(manager_required)])
def update_order_item(order_item_id: int, order_item: OrderItemCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE OrderItems SET OrderID=%s, ProductID=%s, Quantity=%s, UnitPrice=%s WHERE OrderItemID=%s",
                   (order_item.order_id, order_item.product_id, order_item.quantity, order_item.unit_price, order_item_id))
    conn.commit()
    cursor.execute("SELECT * FROM OrderItems WHERE OrderItemID = %s", (order_item_id,))
    updated_order_item = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_order_item


@router.delete("/order_items/{order_item_id}", dependencies=[Depends(manager_required)])
def delete_order_item(order_item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM OrderItems WHERE OrderItemID = %s", (order_item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Order item deleted successfully"}
