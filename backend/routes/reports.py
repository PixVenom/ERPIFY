from fastapi import APIRouter
from backend.database import get_connection
from fastapi import Depends
from backend.auth.role_checker import admin_required, manager_required


router = APIRouter()

@router.get("/reports/sales-summary")
def sales_summary():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DATE(OrderDate) AS Date, COUNT(*) AS TotalOrders, SUM(OI.Quantity * OI.UnitPrice) AS Revenue
        FROM Orders O
        JOIN OrderItems OI ON O.OrderID = OI.OrderID
        GROUP BY DATE(OrderDate)
        ORDER BY Date DESC
    """)
    return cursor.fetchall()

@router.get("/reports/low-stock")
def low_stock(threshold: int = 10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT P.Name, S.Quantity
        FROM Products P
        JOIN Stock S ON P.ProductID = S.ProductID
        WHERE S.Quantity < %s
    """, (threshold,))
    return cursor.fetchall()
