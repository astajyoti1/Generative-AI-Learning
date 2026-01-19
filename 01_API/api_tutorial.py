# FastAPI Basics Tutorial
# This file demonstrates the fundamental concepts of FastAPI, a modern web framework for building APIs with Python.
# FastAPI is built on top of Starlette and Pydantic, providing automatic API documentation, validation, and high performance.

# Theory Overview:
# - FastAPI uses type hints for automatic request validation and API documentation.
# - It generates interactive API docs at /docs (Swagger UI) and /redoc.
# - Supports async operations for better performance.
# - Automatic JSON serialization/deserialization.

# HTTP Methods Theory:
# HTTP methods define the type of operation to be performed on a resource. Here are the main ones used in REST APIs:
#
# 1. GET - Retrieve data from the server
#    - Safe and idempotent (can be called multiple times without side effects)
#    - Used for: Reading/fetching data, listing resources, searching
#    - No request body needed
#    - Parameters can be passed via URL path or query strings
#    - Example: Get user profile, list products, search items
#
# 2. POST - Create new resources on the server
#    - Not idempotent (calling multiple times creates multiple resources)
#    - Used for: Creating new items, submitting forms, uploading data
#    - Request body contains the data to create
#    - Returns the created resource (often with generated ID)
#    - Example: Create new user account, add product to cart, submit contact form
#
# 3. PUT - Update/replace entire resources
#    - Idempotent (multiple calls have same effect as one)
#    - Used for: Updating complete resources, replacing existing data
#    - Request body contains the complete updated resource
#    - Creates resource if it doesn't exist (full replacement)
#    - Example: Update user profile, modify product details
#
# 4. DELETE - Remove resources from the server
#    - Idempotent (deleting something already deleted has no effect)
#    - Used for: Removing items, deleting accounts, clearing data
#    - Usually no request body
#    - Returns success status even if resource didn't exist
#    - Example: Delete user account, remove product, clear cache
#
# Additional common methods:
# - PATCH: Partial updates (modify only specified fields)
# - HEAD: Same as GET but returns only headers (for checking resource existence)
# - OPTIONS: Get information about supported methods for a resource
#
# Usage Guidelines:
# - Use GET for safe read operations
# - Use POST for creating new resources
# - Use PUT for full updates/replacements
# - Use DELETE for removing resources
# - Use PATCH for partial modifications
# - Follow REST conventions for predictable API design

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sqlite3
import json

# Database setup
DATABASE = "api_tutorial.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            is_offer BOOLEAN
        )
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            full_name TEXT
        )
    ''')
    
    # Insert dummy data for items
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        dummy_items = [
            ("Laptop", 999.99, True),
            ("Mouse", 25.50, False),
            ("Keyboard", 75.00, True),
            ("Monitor", 299.99, False),
            ("Headphones", 149.99, True)
        ]
        cursor.executemany("INSERT INTO items (name, price, is_offer) VALUES (?, ?, ?)", dummy_items)
    
    # Insert dummy data for users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        dummy_users = [
            ("john_doe", "john@example.com", "John Doe"),
            ("jane_smith", "jane@example.com", "Jane Smith"),
            ("alice_wonder", "alice@example.com", "Alice Wonderland")
        ]
        cursor.executemany("INSERT INTO users (username, email, full_name) VALUES (?, ?, ?)", dummy_users)
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Create a FastAPI application instance
# This is the main entry point for your API
app = FastAPI(
    title="FastAPI Basics Tutorial",
    description="A simple API to learn FastAPI fundamentals",
    version="1.0.0"
)

# Pydantic models for request/response validation
# These define the structure of data sent to/received from the API

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    is_offer: Optional[bool] = None

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    full_name: Optional[str] = None

# Basic GET route - Hello World
# GET Method Usage: Retrieves data without modifying server state
# Routes are defined using decorators. This responds to GET requests at the root path "/"
@app.get("/")
def read_root():
    """Basic GET endpoint that returns a welcome message."""
    return {"message": "Welcome to FastAPI Basics Tutorial!"}

# GET route to list all items
@app.get("/items/")
def list_items():
    """
    GET endpoint to retrieve all items.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, is_offer FROM items")
    rows = cursor.fetchall()
    conn.close()
    
    items = [Item(id=row[0], name=row[1], price=row[2], is_offer=bool(row[3]) if row[3] is not None else None) for row in rows]
    return {"items": items, "count": len(items)}

# GET route to list all items
@app.get("/items/")
def list_items():
    """
    GET endpoint to retrieve all items.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, is_offer FROM items")
    rows = cursor.fetchall()
    conn.close()
    
    items = [Item(id=row[0], name=row[1], price=row[2], is_offer=bool(row[3]) if row[3] is not None else None) for row in rows]
    return {"items": items, "count": len(items)}
    """
    GET endpoint with path parameter and optional query parameter.

    - item_id: Integer path parameter (required)
    - q: Optional string query parameter
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, is_offer FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        item = Item(id=row[0], name=row[1], price=row[2], is_offer=bool(row[3]) if row[3] is not None else None)
        return {"item": item, "q": q}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# POST route with request body
# POST Method Usage: Creates new resources on the server
# POST requests typically send data in the request body
# FastAPI automatically validates and parses JSON into the Pydantic model
@app.post("/items/")
def create_item(item: Item):
    """
    POST endpoint that accepts an Item in the request body.

    The Item model ensures:
    - name: string (required)
    - price: float (required)
    - is_offer: boolean (optional)
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price, is_offer) VALUES (?, ?, ?)", 
                   (item.name, item.price, item.is_offer))
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"item": Item(id=item_id, name=item.name, price=item.price, is_offer=item.is_offer), "message": "Item created successfully"}

# PUT route - Update operation
# PUT Method Usage: Updates/replaces entire resources (full replacement)
# PUT is used for updating existing resources
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """
    PUT endpoint to update an existing item.

    Combines path parameter (item_id) with request body (item data).
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, price = ?, is_offer = ? WHERE id = ?", 
                   (item.name, item.price, item.is_offer, item_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")
    conn.commit()
    conn.close()
    
    return {"item_id": item_id, "item": item, "message": "Item updated"}

# DELETE route - Delete operation
# DELETE Method Usage: Removes resources from the server
# DELETE removes a resource
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    DELETE endpoint to remove an item by ID.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")
    conn.commit()
    conn.close()
    
    return {"message": f"Item {item_id} deleted"}

# GET route with multiple query parameters
# GET Method Usage: Retrieves filtered/search results using query parameters
# Query parameters are key-value pairs after the ? in the URL
@app.get("/search/")
def search_items(name: Optional[str] = None, price_min: Optional[float] = None, price_max: Optional[float] = None):
    """
    GET endpoint demonstrating multiple optional query parameters.

    Example usage: /search/?name=apple&price_min=1.0&price_max=10.0
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    query = "SELECT id, name, price, is_offer FROM items WHERE 1=1"
    params = []
    
    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if price_min is not None:
        query += " AND price >= ?"
        params.append(price_min)
    if price_max is not None:
        query += " AND price <= ?"
        params.append(price_max)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    items = [Item(id=row[0], name=row[1], price=row[2], is_offer=bool(row[3]) if row[3] is not None else None) for row in rows]
    
    return {
        "items": items,
        "filters": {
            "name": name,
            "price_min": price_min,
            "price_max": price_max
        },
        "count": len(items)
    }

# POST route with user data
# POST Method Usage: Creates new user resources
# Demonstrates using a different Pydantic model
@app.post("/users/")
def create_user(user: User):
    """
    POST endpoint for creating a new user.

    Shows how to use different models for different endpoints.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, full_name) VALUES (?, ?, ?)", 
                       (user.username, user.email, user.full_name))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"user": User(id=user_id, username=user.username, email=user.email, full_name=user.full_name), "message": "User created"}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")

# Async endpoint example
# GET Method Usage: Retrieves data asynchronously for better performance
# FastAPI supports async functions for better performance with I/O operations
@app.get("/async-example/")
async def async_example():
    """
    Async GET endpoint.

    Async functions allow the server to handle other requests while waiting for I/O.
    Useful for database queries, external API calls, etc.
    """
    # Simulate some async operation (in real code, this might be a database query)
    return {"message": "This is an async response"}

# Response with custom status code
# GET Method Usage: Retrieves resource status or existence information
# By default, FastAPI returns 200 for successful operations
# You can specify different status codes
from fastapi import HTTPException

@app.get("/items/{item_id}/status")
def read_item_with_status(item_id: int):
    """
    GET endpoint that demonstrates custom response handling.

    In a real application, you might check if the item exists in a database.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM items WHERE id = ?", (item_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    
    if not exists:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "status": "found"}

# Instructions for running this API:
# 1. Make sure you have FastAPI and Uvicorn installed:
#    pip install fastapi uvicorn
#
# 2. Run the server with auto-reload:
#    uvicorn api_tutorial:app --reload
#    (or use: python -m uvicorn api_tutorial:app --reload)
#
# 3. Open your browser to:
#    - API docs (interactive): http://127.0.0.1:8000/docs
#    - Alternative docs: http://127.0.0.1:8000/redoc
#    - API root: http://127.0.0.1:8000/
#
# 4. Test the endpoints using the docs interface or tools like curl/Postman:
#    - GET / : Basic hello world
#    - GET /items/ : List all items (includes dummy data)
#    - GET /items/1 : Get specific item by ID
#    - POST /items/ : Create new item (updates database)
#    - PUT /items/1 : Update existing item
#    - DELETE /items/1 : Delete item
#    - GET /search/?name=laptop : Search items
#    - POST /users/ : Create new user (updates database)
#    - GET /async-example/ : Async endpoint
#    - GET /items/999/status : Check item existence
#
# Database Features:
# - SQLite database (api_tutorial.db) is created automatically
# - Dummy records are inserted on first run
# - POST endpoints update the database with new records
# - All CRUD operations are functional with persistent storage
#
# Key Concepts Covered:
# - Route definitions (GET, POST, PUT, DELETE)
# - Path parameters
# - Query parameters
# - Request bodies with Pydantic models
# - Response models
# - Async functions
# - Error handling
# - Automatic API documentation
# - Type validation

# To run the uvicorn command, use the following line in your terminal:
# cd D:\GITHUB\Generative-AI-Learning\01_API; & C:/Users/astaj/AppData/Local/Programs/Python/Python313/python.exe -m uvicorn api_tutorial:app --reload