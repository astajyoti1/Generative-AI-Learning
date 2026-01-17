# FastAPI Basics Tutorial
# This file demonstrates the fundamental concepts of FastAPI, a modern web framework for building APIs with Python.
# FastAPI is built on top of Starlette and Pydantic, providing automatic API documentation, validation, and high performance.

# Theory Overview:
# - FastAPI uses type hints for automatic request validation and API documentation.
# - It generates interactive API docs at /docs (Swagger UI) and /redoc.
# - Supports async operations for better performance.
# - Automatic JSON serialization/deserialization.

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

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
    name: str
    price: float
    is_offer: Optional[bool] = None

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

# Basic GET route - Hello World
# Routes are defined using decorators. This responds to GET requests at the root path "/"
@app.get("/")
def read_root():
    """Basic GET endpoint that returns a welcome message."""
    return {"message": "Welcome to FastAPI Basics Tutorial!"}

# GET route with path parameters
# Path parameters are part of the URL path, enclosed in curly braces {}
# They are automatically validated and converted to the specified type
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    """
    GET endpoint with path parameter and optional query parameter.

    - item_id: Integer path parameter (required)
    - q: Optional string query parameter
    """
    return {"item_id": item_id, "q": q}

# POST route with request body
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
    return {"item": item, "message": "Item created successfully"}

# PUT route - Update operation
# PUT is used for updating existing resources
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """
    PUT endpoint to update an existing item.

    Combines path parameter (item_id) with request body (item data).
    """
    return {"item_id": item_id, "item": item, "message": "Item updated"}

# DELETE route - Delete operation
# DELETE removes a resource
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    DELETE endpoint to remove an item by ID.
    """
    return {"message": f"Item {item_id} deleted"}

# GET route with multiple query parameters
# Query parameters are key-value pairs after the ? in the URL
@app.get("/search/")
def search_items(name: Optional[str] = None, price_min: Optional[float] = None, price_max: Optional[float] = None):
    """
    GET endpoint demonstrating multiple optional query parameters.

    Example usage: /search/?name=apple&price_min=1.0&price_max=10.0
    """
    return {
        "filters": {
            "name": name,
            "price_min": price_min,
            "price_max": price_max
        },
        "message": "Search results would be returned here"
    }

# POST route with user data
# Demonstrates using a different Pydantic model
@app.post("/users/")
def create_user(user: User):
    """
    POST endpoint for creating a new user.

    Shows how to use different models for different endpoints.
    """
    return {"user": user, "message": "User created"}

# Async endpoint example
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
# By default, FastAPI returns 200 for successful operations
# You can specify different status codes
from fastapi import HTTPException

@app.get("/items/{item_id}/status")
def read_item_with_status(item_id: int):
    """
    GET endpoint that demonstrates custom response handling.

    In a real application, you might check if the item exists in a database.
    """
    if item_id == 999:
        # Raise HTTPException for error responses
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "status": "found"}

# Instructions for running this API:
# 1. Make sure you have FastAPI and Uvicorn installed:
#    pip install fastapi uvicorn
#
# 2. Run the server with auto-reload:
#    uvicorn test:app --reload
#    (or use: python -m uvicorn test:app --reload)
#
# 3. Open your browser to:
#    - API docs (interactive): http://127.0.0.1:8000/docs
#    - Alternative docs: http://127.0.0.1:8000/redoc
#    - API root: http://127.0.0.1:8000/
#
# 4. Test the endpoints using the docs interface or tools like curl/Postman:
#    - GET / : Basic hello world
#    - GET /items/123 : Path parameter example
#    - GET /items/123?q=search : Path + query parameters
#    - POST /items/ : Send JSON {"name": "apple", "price": 1.50}
#    - PUT /items/123 : Update with JSON body
#    - DELETE /items/123 : Delete example
#    - GET /search/?name=apple&price_min=1.0 : Query parameters
#    - POST /users/ : Create user with JSON
#    - GET /async-example/ : Async endpoint
#    - GET /items/999/status : Error handling example
#
# 5. To stop the server: Press Ctrl+C in the terminal
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
# cd D:\GITHUB\Generative-AI-Learning\01_API; & C:/Users/astaj/AppData/Local/Programs/Python/Python313/python.exe -m uvicorn test:app --reload