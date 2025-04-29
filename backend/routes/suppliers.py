from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.schemas import SupplierCreate, SupplierOut
from auth.role_checker import manager_required
from backend.utils.db import get_connection

router = APIRouter()


@router.post("/suppliers", response_model=SupplierOut, dependencies=[Depends(manager_required)])
def create_supplier(supplier: SupplierCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO suppliers (supplier_id, name, email, phone, address) VALUES (%d,%s,%s,%d,%s)",
                   (supplier.name, supplier.email, supplier.phone, supplier.address))
    conn.commit()
    cursor.execute("SELECT * FROM suppliers WHERE supplier_id = LAST_INSERT_ID()")
    new_supplier = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_supplier


@router.get("/suppliers", response_model=List[SupplierOut], dependencies=[Depends(manager_required)])
def get_suppliers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    cursor.close()
    conn.close()
    return suppliers


@router.get("/suppliers/{supplier_id}", response_model=SupplierOut, dependencies=[Depends(manager_required)])
def get_supplier(supplier_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %d", (supplier_id,))
    supplier = cursor.fetchone()
    cursor.close()
    conn.close()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.put("/suppliers/{supplier_id}", response_model=SupplierOut, dependencies=[Depends(manager_required)])
def update_supplier(supplier_id: int, supplier: SupplierCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE suppliers SET name=%s, email=%s, phone=%s, address=%s WHERE supplier_id=%d",
                   (supplier.name, supplier.email, supplier.phone, supplier.address, supplier_id))
    conn.commit()
    cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %d", (supplier_id,))
    updated_supplier = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_supplier


@router.delete("/suppliers/{supplier_id}", dependencies=[Depends(manager_required)])
def delete_supplier(supplier_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM suppliers WHERE supplier_id = %d", (supplier_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Supplier deleted successfully"}
