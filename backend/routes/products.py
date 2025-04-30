from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import ProductCreate, ProductOut
from backend.auth.role_checker import manager_required
from backend.utils.db import get_connection

router = APIRouter()


@router.post("/products/", response_model=ProductOut, dependencies=[Depends(manager_required)])
def create_product(product: ProductCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        insert_query = """
        INSERT INTO products (product_id, name, category, price, supplier_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            product.product_id,
            product.name,
            product.category,
            product.price,
            product.supplier_id
        ))
        conn.commit()

        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product.product_id,))
        new_product = cursor.fetchone()

        cursor.close()
        conn.close()

        if not new_product:
            raise HTTPException(status_code=500, detail="Failed to fetch the created product")

        return new_product

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")


@router.get("/products", response_model=List[ProductOut], dependencies=[Depends(manager_required)])
def get_products():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        cursor.close()
        conn.close()

        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


@router.get("/products/{product_id}", response_model=ProductOut, dependencies=[Depends(manager_required)])
def get_product(product_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()

        cursor.close()
        conn.close()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")


@router.put("/products/{product_id}", response_model=ProductOut, dependencies=[Depends(manager_required)])
def update_product(product_id: int, product: ProductCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        update_query = """
        UPDATE products SET name = %s, category = %s, price = %s, supplier_id = %s
        WHERE product_id = %s
        """
        cursor.execute(update_query, (
            product.name,
            product.category,
            product.price,
            product.supplier_id,
            product_id
        ))
        conn.commit()

        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        updated_product = cursor.fetchone()

        cursor.close()
        conn.close()

        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")

        return updated_product

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")


@router.delete("/products/{product_id}", dependencies=[Depends(manager_required)])
def delete_product(product_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Product deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")