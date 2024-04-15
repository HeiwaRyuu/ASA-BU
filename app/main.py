from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()


def read_objects_from_json(path):
    if not os.path.isfile(path):
        open(path, "w+").close()

    with open(path, "r+", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception as e:
            print(e)
            return []

def write_object_to_json(item, path, keep=True):
    if keep:
        prev_json = read_objects_from_json(path)
        prev_json.append(item)
    else:
        prev_json = item
    with open(path, "w+", encoding="utf-8") as f:
        json.dump(prev_json, f, ensure_ascii=False, indent=4, separators=(",", ": "))

def delete_object_from_json(item_id, path):
    json_items = read_objects_from_json(path)
    print(json_items)
    if json_items:
        for i in range(len(json_items)):
            if json_items[i]["id"] == item_id:
                item_data = json_items.pop(i)
                write_object_to_json(json_items, path, keep=False)
                return item_data
    return f"No item ID {item_id}"

class Item(BaseModel):
    id: int
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items")
def read_items():
    items = read_objects_from_json("items.json")
    return {"Items:" : items}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    write_object_to_json(json.loads(item.model_dump_json()), "items.json")
    return {"item_name": item.name, "item_id": item_id}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    json_item = delete_object_from_json(item_id, "items.json")
    return {"item": json_item}
