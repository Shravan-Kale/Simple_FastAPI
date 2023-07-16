import json
from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel


class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()

with open('database.json', 'r') as f:
    database = json.load(f)


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.post("/items/")
async def create_item(item: Item):
    i_id = max([i['id'] for i in database]) + 1
    new_item = {
        "id": i_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax
    }
    database.append(new_item)
    with open("database.json", 'w') as f:
        json.dump(database, f)
    return new_item


@app.get("/items/")
async def get_all_items():
    return database


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = [i for i in database if i["id"] == item_id]
    return item[0] if len(item) > 0 else {}


@app.put("/items/{item_id}")
async def update_item(item_id: int, new_item: Item):
    item = [i for i in database if i["id"] == item_id][0]
    if item:
        database.remove(item)
        new_item = {
            "id": item_id,
            "name": new_item.name,
            "description": new_item.description,
            "price": new_item.price,
            "tax": new_item.tax
        }
        database.append(new_item)
    with open('database.json', 'w') as f:
        json.dump(database, f)
    return new_item


@app.get("/search")
async def search_item(name: Optional[str] = Query(None, title="Name", description="Name of the product looking for"),
                      description: Optional[str] = Query(None, title="Description", description="description of the "
                                                                                                "product looking for"),
                      price: Optional[int] = Query(None, title="Price", description="price of the product looking for"),
                      tax: Optional[int] = Query(None, title="Tax", description="tax of the product looking for")):
    item = []
    if name:
        item = [i for i in database if i["name"].lower() == name.lower()]
    if description:
        if item:
            item = [i for i in item if i["description"].lower() == description.lower()]
        else:
            item = [i for i in database if i["description"].lower() == description.lower()]
    if price:
        if item:
            item = [i for i in item if i["price"] == price]
        else:
            item = [i for i in database if i["price"] == price]
    if tax:
        if item:
            item = [i for i in item if i["tax"] == tax]
        else:
            item = [i for i in database if i["tax"] == tax]
    return item


@app.delete("/delete/{item_id")
async def delete_item(item_id: int):
    item = [i for i in database if i["id"] == item_id]
    if item:
        database.remove(item[0])
    with open("database.json", 'w') as f:
        json.dump(database, f)
    return item[0] if len(item) > 0 else {}
