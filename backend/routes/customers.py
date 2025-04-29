from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import CustomerCreate, CustomerOut
from backend.auth.role_checker import manager_required
from backend.utils.db import get_connection

router = APIRouter()


@router.post("/customers", response_model=CustomerOut, dependencies=[Depends(manager_required)])
def create_customer(customer: CustomerCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO customers (customer_id,name,email,phone,address) VALUES (%s, %s, %s, %s,%s)",
                   (customer.customer_id,customer.name,customer.email,customer.phone,customer.address))
    conn.commit()
    cursor.execute("SELECT * FROM customers WHERE customer_id = LAST_INSERT_ID()")
    new_customer = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_customer


@router.get("/customers", response_model=List[CustomerOut], dependencies=[Depends(manager_required)])
def get_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return customers


@router.get("/customers/{customer_id}", response_model=CustomerOut, dependencies=[Depends(manager_required)])
def get_customer(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/customers/{customer_id}", response_model=CustomerOut, dependencies=[Depends(manager_required)])
def update_customer(customer_id: int, customer: CustomerCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE customers SET customer_id=%d, name=%s, email=%s, phone=%d WHERE customer_id=%d",
                   (customer.name, customer.email, customer.phone, customer.address, customer_id))
    conn.commit()
    cursor.execute("SELECT * FROM customers WHERE customer_id = %d", (customer_id,))
    updated_customer = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_customer


@router.delete("/customers/{customer_id}", dependencies=[Depends(manager_required)])
def delete_customer(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE customer_id = %d", (customer_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Customer deleted successfully"}