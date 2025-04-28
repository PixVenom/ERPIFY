from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import InvoiceCreate, InvoiceOut
from backend.auth.role_checker import manager_required
from backend.utils.db import get_connection

router = APIRouter()


@router.post("/invoices", response_model=InvoiceOut, dependencies=[Depends(manager_required)])
def create_invoice(invoice: InvoiceCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO Invoices (OrderID, InvoiceDate, TotalAmount, PaymentStatus) VALUES (%s, %s, %s, %s)",
                   (invoice.order_id, invoice.invoice_date, invoice.total_amount, invoice.payment_status))
    conn.commit()
    cursor.execute("SELECT * FROM Invoices WHERE InvoiceID = LAST_INSERT_ID()")
    new_invoice = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_invoice


@router.get("/invoices", response_model=List[InvoiceOut], dependencies=[Depends(manager_required)])
def get_invoices():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Invoices")
    invoices = cursor.fetchall()
    cursor.close()
    conn.close()
    return invoices


@router.get("/invoices/{invoice_id}", response_model=InvoiceOut, dependencies=[Depends(manager_required)])
def get_invoice(invoice_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Invoices WHERE InvoiceID = %s", (invoice_id,))
    invoice = cursor.fetchone()
    cursor.close()
    conn.close()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.put("/invoices/{invoice_id}", response_model=InvoiceOut, dependencies=[Depends(manager_required)])
def update_invoice(invoice_id: int, invoice: InvoiceCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE Invoices SET OrderID=%s, InvoiceDate=%s, TotalAmount=%s, PaymentStatus=%s WHERE InvoiceID=%s",
                   (invoice.order_id, invoice.invoice_date, invoice.total_amount, invoice.payment_status, invoice_id))
    conn.commit()
    cursor.execute("SELECT * FROM Invoices WHERE InvoiceID = %s", (invoice_id,))
    updated_invoice = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_invoice


@router.delete("/invoices/{invoice_id}", dependencies=[Depends(manager_required)])
def delete_invoice(invoice_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Invoices WHERE InvoiceID = %s", (invoice_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Invoice deleted successfully"}
