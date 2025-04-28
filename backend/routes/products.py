from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import ProductCreate, ProductOut
from backend.auth.role_checker import manager_required
from backend.utils.db import get_connection

router = APIRouter()


@router.post("/products", response_model=ProductOut, dependencies=[Depends(manager_required)])
def create_product(product: ProductCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO Products (Name, Category, Price, SupplierID) VALUES (%s, %s, %s, %s)",
                   (product.name, product.category, product.price, product.supplier_id))
    conn.commit()
    cursor.execute("SELECT * FROM Products WHERE ProductID = LAST_INSERT_ID()")
    new_product = cursor.fetchone()
    cursor.close()
    conn.close()
    return new_product


@router.get("/products", response_model=List[ProductOut], dependencies=[Depends(manager_required)])
def get_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


@router.get("/products/{product_id}", response_model=ProductOut, dependencies=[Depends(manager_required)])
def get_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Products WHERE ProductID = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=ProductOut, dependencies=[Depends(manager_required)])
def update_product(product_id: int, product: ProductCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE Products SET Name=%s, Category=%s, Price=%s, SupplierID=%s WHERE ProductID=%s",
                   (product.name, product.category, product.price, product.supplier_id, product_id))
    conn.commit()
    cursor.execute("SELECT * FROM Products WHERE ProductID = %s", (product_id,))
    updated_product = cursor.fetchone()
    cursor.close()
    conn.close()
    return updated_product


@router.delete("/products/{product_id}", dependencies=[Depends(manager_required)])
def delete_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Products WHERE ProductID = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Product deleted successfully"}
