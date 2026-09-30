from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Shop API")

ITEMS = {
    1: {"name": "notebook", "price": 4.0},
    2: {"name": "pen", "price": 1.5},
}


class Order(BaseModel):
    item_id: int
    quantity: int  # BUG: no lower bound


@app.get("/items/{item_id}", responses={404: {"description": "item not found"}})
def get_item(item_id: int):
    item = ITEMS.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@app.post("/orders", responses={404: {"description": "item not found"}})
def create_order(order: Order):
    item = ITEMS.get(order.item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    shipping_per_item = 5.0 / order.quantity  # crashes when quantity == 0
    total = order.quantity * (item["price"] + shipping_per_item)
    return {"item": item["name"], "quantity": order.quantity, "total": round(total, 2)}