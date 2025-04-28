from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import StockCreate, StockOut
from backend.auth.role_checker import manager_required
from backend.utils.db import get_connection

router = APIRouter()


@router.post("/stock", response_model=StockOut, dependencies=[Depends(manager_required)])
def add_stock(stock: StockCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO Stock (ProductID, Quantity) VALUES (%s, %s)",
                   (stock.product_id, stock.quantity))
    conn.commit()
    cursor.execute("SELECT * FROM Stock WHERE StockID = LAST_INSERT_ID()")
    new_stock = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_stock


@router.get("/stock", response_model=List[StockOut], dependencies=[Depends(manager_required)])
def get_all_stock():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Stock")
    stock_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return stock_list


@router.get("/stock/{stock_id}", response_model=StockOut, dependencies=[Depends(manager_required)])
def get_stock(stock_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Stock WHERE StockID = %s", (stock_id,))
    stock = cursor.fetchone()
    cursor.close()
    conn.close()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock item not found")
    return stock


@router.put("/stock/{stock_id}", response_model=StockOut, dependencies=[Depends(manager_required)])
def update_stock(stock_id: int, stock: StockCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE Stock SET ProductID=%s, Quantity=%s WHERE StockID=%s",
                   (stock.product_id, stock.quantity, stock_id))
    conn.commit()
    cursor.execute("SELECT * FROM Stock WHERE StockID = %s", (stock_id,))
    updated_stock = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_stock


@router.delete("/stock/{stock_id}", dependencies=[Depends(manager_required)])
def delete_stock(stock_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Stock WHERE StockID = %s", (stock_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Stock item deleted successfully"}
