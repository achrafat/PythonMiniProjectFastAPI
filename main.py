from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


 #Pydantic model for an item
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True
class ItemResponse(BaseModel):
    name: str
    price: float
    in_stock: bool    

# In-memory "database"
items: List[Item] = []

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Python MiniProject with FastAPI"}

# List all items
@app.get("/items/",response_model=List[ItemResponse])
def get_items():
    return items

# Get an item by ID
@app.get("/items/{item_id}",response_model=ItemResponse)
def get_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# Create a new item
@app.post("/items/",response_model=ItemResponse)
def create_item(item: Item):
    items.append(item)
    return {"message": "Item added successfully", "item": item}

# Update an existing item
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = updated_item
    return {"message": "Item updated successfully", "item": updated_item}

# Delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items.pop(item_id)
    return {"message": "Item deleted successfully", "item": deleted_item}
g