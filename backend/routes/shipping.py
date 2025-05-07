from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import ShippingCreate, ShippingOut
from backend.auth.role_checker import manager_required
from backend.database import get_connection

router = APIRouter()


@router.post("/shipping", response_model=ShippingOut, dependencies=[Depends(manager_required)])
def create_shipping(shipping: ShippingCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        INSERT INTO shipping (invoice_id, shipping_date, shipping_status)
        VALUES (%s, %s, %s)
    """, (shipping.invoice_id, shipping.shipping_date, shipping.shipping_status))
    conn.commit()
    cursor.execute("SELECT * FROM shipping WHERE shipping_id = LAST_INSERT_ID()")
    new_shipping = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_shipping


@router.get("/shipping", response_model=List[ShippingOut], dependencies=[Depends(manager_required)])
def get_all_shipping():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM shipping")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records


@router.get("/shipping/{shipping_id}", response_model=ShippingOut, dependencies=[Depends(manager_required)])
def get_shipping(shipping_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM shipping WHERE shipping_id = %s", (shipping_id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if not record:
        raise HTTPException(status_code=404, detail="Shipping record not found")
    return record


@router.delete("/shipping/{shipping_id}", dependencies=[Depends(manager_required)])
def delete_shipping(shipping_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shipping WHERE shipping_id = %s", (shipping_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Shipping record deleted successfully"}