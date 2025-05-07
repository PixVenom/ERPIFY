from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import CustomerCreate, CustomerOut
from backend.auth.role_checker import JWTBearer
from backend.database import get_connection

router = APIRouter()

@router.post("/customers", response_model=CustomerOut, dependencies=[Depends(JWTBearer(["manager", "admin", "staff"]))])
def create_customer(customer: CustomerCreate):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)",
            (customer.name, customer.email, customer.phone, customer.address)
        )
        connection.commit()

        new_customer_id = cursor.lastrowid  # Get the ID of the newly inserted customer
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (new_customer_id,))
        new_customer = cursor.fetchone()
        
        if not new_customer:
            raise HTTPException(status_code=500, detail="Customer not found after insert")
        return new_customer
    finally:
        cursor.close()
        connection.close()

@router.get("/customers", response_model=List[CustomerOut], dependencies=[Depends(JWTBearer(["manager", "admin", "staff"]))])
def get_customers():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM customers")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

@router.get("/customers/{customer_id}", response_model=CustomerOut, dependencies=[Depends(JWTBearer(["manager", "admin", "staff"]))])
def get_customer(customer_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    finally:
        cursor.close()
        connection.close()

@router.put("/customers/{customer_id}", response_model=CustomerOut, dependencies=[Depends(JWTBearer(["manager", "admin", "staff"]))])
def update_customer(customer_id: int, customer: CustomerCreate):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE customers SET name=%s, email=%s, phone=%s, address=%s WHERE customer_id=%s",
            (customer.name, customer.email, customer.phone, customer.address, customer_id)
        )
        connection.commit()
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        updated_customer = cursor.fetchone()
        if not updated_customer:
            raise HTTPException(status_code=404, detail="Updated customer not found")
        return updated_customer
    finally:
        cursor.close()
        connection.close()

@router.delete("/customers/{customer_id}", dependencies=[Depends(JWTBearer(["manager", "admin", "staff"]))])
def delete_customer(customer_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
        connection.commit()
        return {"message": "Customer deleted successfully"}
    finally:
        cursor.close()
        connection.close()