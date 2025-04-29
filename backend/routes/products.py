from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import ProductCreate, ProductOut
from backend.auth.role_checker import manager_required
from backend.utils.db import get_connection

router = APIRouter()

# POST endpoint for creating a new product
@router.post("/products/", response_model=ProductOut, dependencies=[Depends(manager_required)])
def create_product(product: ProductCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Insert product into database
        cursor.execute("INSERT INTO products (product_id, name, category, price, supplier_id) VALUES (%d, %s, %s, %d, %d)",
                       (product.product_id,product.name,product.category,product.category,product.price,product.supplier_id))
        conn.commit()

        # Get the newly inserted product
        cursor.execute("SELECT * FROM products WHERE product_id = LAST_INSERT_ID()")
        new_product = cursor.fetchone()
        
        # Close cursor and connection
        cursor.close()
        conn.close()

        # Check if the product was successfully created
        if not new_product:
            raise HTTPException(status_code=500, detail="Failed to fetch the created product")

        return new_product

    except Exception as e:
        # Handle any error that occurs during the process
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")


# GET endpoint for fetching all products
@router.get("/products", response_model=List[ProductOut], dependencies=[Depends(manager_required)])
def get_products():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch all products from the database
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        return products

    except Exception as e:
        # Handle any error that occurs during the process
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


# GET endpoint for fetching a specific product by its ID
@router.get("/products/{product_id}", response_model=ProductOut, dependencies=[Depends(manager_required)])
def get_product(product_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch the product by ID
        cursor.execute("SELECT * FROM products WHERE product_id = %d", (product_id,))
        product = cursor.fetchone()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # If no product found, raise 404 error
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    except Exception as e:
        # Handle any error that occurs during the process
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")


# PUT endpoint for updating an existing product
@router.put("/products/{product_id}", response_model=ProductOut, dependencies=[Depends(manager_required)])
def update_product(product_id: int, product: ProductCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Update product in the database
        cursor.execute(
            "UPDATE products SET product_id=%d, name=%s, category=%s, price=%d, supplier_id=%d WHERE product_id=%d",
            (product.name, product.category, product.price, product.supplier_id, product_id)
        )
        conn.commit()

        # Fetch the updated product
        cursor.execute("SELECT * FROM products WHERE product_id = %d", (product_id,))
        updated_product = cursor.fetchone()

        # Close cursor and connection
        cursor.close()
        conn.close()

        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")

        return updated_product

    except Exception as e:
        # Handle any error that occurs during the process
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")


# DELETE endpoint for deleting a product by ID
@router.delete("/products/{product_id}", dependencies=[Depends(manager_required)])
def delete_product(product_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Delete the product from the database
        cursor.execute("DELETE FROM products WHERE product_id = %d", (product_id,))
        conn.commit()

        # Close cursor and connection
        cursor.close()
        conn.close()

        return {"message": "Product deleted successfully"}

    except Exception as e:
        # Handle any error that occurs during the process
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")